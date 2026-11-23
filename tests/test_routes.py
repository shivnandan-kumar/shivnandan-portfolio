"""Tests for the portfolio's public pages."""

import pytest

from app import create_app
from email_service import send_contact_message


@pytest.fixture()
def client():
    """Provide a test client for an isolated Flask application."""
    app = create_app()
    app.config.update(
        TESTING=True,
        WEB3FORMS_ACCESS_KEY="test-public-key-placeholder",
    )

    with app.test_client() as test_client:
        yield test_client


def test_home_page_returns_successful_response(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Shivnandan Kumar" in response.data


def test_contact_form_renders_web3forms_fields_and_accessible_controls(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'action="https://api.web3forms.com/submit"' not in response.data
    assert b'method="post"' not in response.data
    assert b'<button class="contact-submit" type="button">' in response.data
    assert b'Send message <span class="contact-submit-arrow" aria-hidden="true">' in response.data
    assert b"Please enable JavaScript to send a message." in response.data
    assert b'name="access_key" value="test-public-key-placeholder"' in response.data
    assert b'id="contact-name"' in response.data
    assert b'id="contact-email"' in response.data
    assert b'id="contact-message"' in response.data
    assert b'aria-hidden="true"' in response.data
    assert b'name="website"' in response.data
    assert b'minlength="20"' in response.data
    assert b'id="contact-status"' in response.data
    assert b'/static/js/contact-form.js' in response.data


def test_contact_submission_no_longer_posts_to_flask_or_uses_csrf_token(client):
    page = client.get("/")
    response = client.post("/", data={"message": "form submission bypasses Flask"})

    assert b'name="csrf_token"' not in page.data
    assert response.status_code == 405


def test_web3forms_client_script_validates_honeypot_and_handles_api_results(client):
    response = client.get("/static/js/contact-form.js")
    script = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'fetch("https://api.web3forms.com/submit"' in script
    assert '"Content-Type": "application/json"' in script
    assert 'form.reportValidity()' in script
    assert 'form.querySelector(\'[name="website"]\')' in script
    assert 'form.querySelector(".contact-submit")' in script
    assert 'if (honeypot.value.trim()) return;' in script
    assert 'submitButton.type = "submit";' in script
    assert script.index('form.addEventListener("submit"') < script.index('submitButton.type = "submit";')
    assert 'result.success !== true' in script
    assert 'controller.abort(), 15000' in script
    assert "Your message could not be sent right now. Please try again later." in script
    assert "Thanks for reaching out. Your message has been sent." in script
    assert '"csrf_token"' not in script


def test_smtp_delivery_uses_starttls_and_keeps_message_plain_text(monkeypatch):
    from unittest.mock import Mock

    smtp_server = Mock()
    smtp_server.__enter__ = Mock(return_value=smtp_server)
    smtp_server.__exit__ = Mock(return_value=False)
    monkeypatch.setattr("email_service.smtplib.SMTP", lambda *_args, **_kwargs: smtp_server)

    send_contact_message(
        name="A Visitor",
        sender_email="visitor@example.com",
        message="Hello, I would like to discuss a project.",
        config={
            "CONTACT_RECIPIENT": "owner@example.com",
            "SMTP_HOST": "smtp.example.com",
            "SMTP_PORT": 587,
            "SMTP_USERNAME": "sender@example.com",
            "SMTP_PASSWORD": "test-only-password",
        },
    )

    smtp_server.starttls.assert_called_once()
    smtp_server.login.assert_called_once_with("sender@example.com", "test-only-password")
    sent_email = smtp_server.send_message.call_args.args[0]
    assert sent_email["To"] == "owner@example.com"
    assert sent_email["Reply-To"] == "visitor@example.com"
    assert "Hello, I would like to discuss a project." in sent_email.get_content()


def test_primary_navigation_links_to_standalone_pages(client):
    response = client.get("/")

    assert b'<nav aria-label="Primary navigation">' in response.data
    assert b'href="/"' in response.data
    assert b'href="/projects"' in response.data
    assert b'href="/about"' in response.data
    assert b'href="/skills"' in response.data
    assert b'href="/contact"' in response.data
    assert b'id="projects"' in response.data
    assert b'id="about"' in response.data
    assert b'id="skills"' in response.data
    assert b'id="contact"' in response.data
    assert b'aria-label="Home"' in response.data
    assert b'aria-label="Projects"' in response.data
    assert b'aria-label="About"' in response.data
    assert b'aria-label="Skills"' in response.data
    assert b'aria-label="Contact"' in response.data
    assert b'data-tooltip="Home"' in response.data
    assert b'data-tooltip="Projects"' in response.data
    assert b'data-tooltip="About"' in response.data
    assert b'data-tooltip="Skills"' in response.data
    assert b'data-tooltip="Contact"' in response.data


def test_featured_projects_include_confirmed_content(client):
    response = client.get("/")

    assert b"BloodLink" in response.data
    assert b"blood donor search platform" in response.data
    assert b"SQLite (local)" in response.data
    assert b"Supabase PostgreSQL (production)" in response.data
    assert b"E-Governance Complaint and Service Management Portal" in response.data
    assert b"submit complaints and track status" in response.data
    assert b"Supabase PostgreSQL" in response.data


def test_bloodlink_screenshots_are_accessible_and_lazy_loaded(client):
    response = client.get("/")

    assert b'images/projects/bloodlink-home.jpg' in response.data
    assert b'images/projects/bloodlink-how-it-works.jpg' in response.data
    assert response.data.count(b'loading="lazy"') >= 2
    assert b'BloodLink home page showing its donor network overview.' in response.data


def test_featured_projects_link_to_confirmed_repositories_and_demo(client):
    response = client.get("/")

    assert b'href="https://github.com/shivnandan-kumar/bloodlink-flask"' in response.data
    assert b'href="https://github.com/shivnandan-kumar/egovportal"' in response.data
    assert b'href="https://bloodlink-flask.onrender.com/"' in response.data
    assert b'href="https://egovportal-6lpv.onrender.com"' in response.data
    assert b'rel="noopener noreferrer"' in response.data


@pytest.mark.parametrize(
    ("slug", "expected_text"),
    [
        ("bloodlink", b"Pincode-first matching with a city fallback."),
        ("egovernance", b"Complaint status tracking and history timeline."),
    ],
)
def test_project_detail_pages_show_confirmed_case_study_content(client, slug, expected_text):
    response = client.get(f"/projects/{slug}")

    assert response.status_code == 200
    assert expected_text in response.data
    assert b"Key features" in response.data
    assert b"Technology" in response.data
    assert b"View source on GitHub" in response.data


def test_unknown_project_detail_returns_not_found(client):
    response = client.get("/projects/not-a-project")

    assert response.status_code == 404


def test_sitemap_lists_project_case_study_pages(client):
    response = client.get("/sitemap.xml")

    assert response.status_code == 200
    assert b"/projects/bloodlink" in response.data
    assert b"/projects/egovernance" in response.data


def test_home_page_links_to_verified_social_profiles(client):
    response = client.get("/")

    assert b'href="https://github.com/shivnandan-kumar"' in response.data
    assert b'href="https://linkedin.com/in/shivnandan-kumar-27804b3a9"' in response.data


def test_about_section_includes_confirmed_profile_and_education(client):
    response = client.get("/")
    page = " ".join(response.get_data(as_text=True).split())

    assert "Python &amp; Flask<br><span>Developer</span>" in page
    assert "I build practical web applications and backend solutions using Python and Flask, with an emphasis on turning real-world requirements into working software." in page
    assert "I enjoy turning real-world problems into functional applications, with a focus on clean code, database integration, and reliable functionality." in page
    assert "My work includes projects like BloodLink and an E-Governance Complaint and Service Management Portal." in page
    assert b"Bachelor of Computer Applications (BCA)" in response.data
    assert b"Sai Nath University" in response.data
    assert b"Ranchi" in response.data
    assert b"Passing year" in response.data
    assert b">2026<" in response.data
    assert b"education-icon" in response.data


def test_skills_section_lists_confirmed_tools_by_category(client):
    response = client.get("/")

    assert b'Technologies and tools from my development toolkit.' in response.data
    for skill in (
        b"Backend", b"Python", b"Flask", b"SQLAlchemy",
        b"Frontend", b"HTML", b"CSS", b"JavaScript",
        b"Databases", b"PostgreSQL", b"SQLite",
        b"Developer tools", b"Git", b"GitHub", b"VS Code",
        b"Deployment &amp; platform", b"Render", b"Supabase",
    ):
        assert skill in response.data


def test_stylesheet_includes_phone_and_narrow_phone_layouts(client):
    response = client.get("/static/css/styles.css")

    assert response.status_code == 200
    assert b"@media (max-width: 40rem)" in response.data
    assert b"@media (max-width: 22rem)" in response.data
    assert b"grid-template-columns: 1fr" in response.data
    assert b"min-width: 320px" not in response.data


def test_skills_styles_preserve_rows_and_support_responsive_badges(client):
    response = client.get("/static/css/styles.css")

    assert b"grid-template-columns: minmax(0, 1fr)" in response.data
    assert b"@media (min-width: 40.01rem) and (max-width: 56rem)" in response.data
    assert b".skill-list li:hover" in response.data
    assert b"transition: border-color 160ms ease" in response.data
    assert b".skill-list li" in response.data
