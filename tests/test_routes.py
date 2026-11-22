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
        WTF_CSRF_ENABLED=False,
        CONTACT_RECIPIENT="",
        SMTP_HOST="",
        SMTP_USERNAME="",
        SMTP_PASSWORD="",
    )

    with app.test_client() as test_client:
        yield test_client


def test_home_page_returns_successful_response(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Shivnandan Kumar" in response.data


def test_contact_form_renders_accessible_fields_and_csrf_token(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'action="/#contact"' in response.data
    assert b'id="contact-name"' in response.data
    assert b'id="contact-email"' in response.data
    assert b'id="contact-message"' in response.data
    assert b'aria-hidden="true"' in response.data
    assert b'name="website"' in response.data


def test_contact_form_rejects_invalid_email_and_short_message(client):
    response = client.post(
        "/",
        data={"name": "Visitor", "email": "not-an-email", "message": "Too short"},
    )

    assert response.status_code == 400
    assert b"Enter a valid email address." in response.data
    assert b"Message must be between 20 and 3000 characters." in response.data


def test_valid_contact_form_sends_message_and_confirms_success(client, monkeypatch):
    sent = {}

    def capture_message(**message):
        sent.update(message)

    monkeypatch.setattr("app.send_contact_message", capture_message)
    response = client.post(
        "/",
        data={
            "name": "A Visitor",
            "email": "visitor@example.com",
            "message": "Hello, I would like to discuss a project.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Your message has been sent." in response.data
    assert sent["name"] == "A Visitor"
    assert sent["sender_email"] == "visitor@example.com"
    assert sent["message"] == "Hello, I would like to discuss a project."


def test_contact_honeypot_discards_bot_submission(client, monkeypatch):
    def unexpected_send(**_message):
        pytest.fail("Honeypot submission must not be sent.")

    monkeypatch.setattr("app.send_contact_message", unexpected_send)
    response = client.post(
        "/",
        data={
            "name": "Bot",
            "email": "bot@example.com",
            "message": "Automated message pretending to be a visitor.",
            "website": "http://spam.example",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("#contact")


def test_contact_form_reports_unconfigured_delivery_without_false_success(client):
    response = client.post(
        "/",
        data={
            "name": "A Visitor",
            "email": "visitor@example.com",
            "message": "Hello, I would like to discuss a project.",
        },
    )

    assert response.status_code == 503
    assert b"could not be sent right now" in response.data
    assert b"Your message has been sent." not in response.data


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


def test_contact_form_rejects_missing_csrf_token():
    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as csrf_client:
        page = csrf_client.get("/")
        response = csrf_client.post(
            "/",
            data={
                "name": "A Visitor",
                "email": "visitor@example.com",
                "message": "Hello, I would like to discuss a project.",
            },
        )

    assert b'name="csrf_token"' in page.data
    assert response.status_code == 400


def test_primary_navigation_links_to_page_sections(client):
    response = client.get("/")

    assert b'<nav aria-label="Primary navigation">' in response.data
    assert b'href="#home"' in response.data
    assert b'href="#projects"' in response.data
    assert b'href="#about"' in response.data
    assert b'href="#skills"' in response.data
    assert b'href="#contact"' in response.data
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
