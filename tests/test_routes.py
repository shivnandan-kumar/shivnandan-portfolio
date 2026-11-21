"""Tests for the portfolio's public pages."""

import pytest

from app import create_app


@pytest.fixture()
def client():
    """Provide a test client for an isolated Flask application."""
    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_home_page_returns_successful_response(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Shivnandan Kumar" in response.data


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


def test_featured_projects_link_to_confirmed_repositories_and_demo(client):
    response = client.get("/")

    assert b'href="https://github.com/shivnandan-kumar/bloodlink-flask"' in response.data
    assert b'href="https://github.com/shivnandan-kumar/egovportal"' in response.data
    assert b'href="https://bloodlink-flask.onrender.com/"' in response.data
    assert b'href="https://egovportal-6lpv.onrender.com"' in response.data
    assert b'rel="noopener noreferrer"' in response.data
