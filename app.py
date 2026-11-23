"""Flask application entry point for the portfolio."""

import os
import secrets

from flask import Flask, Response, abort, render_template, url_for

from forms import ContactForm
from project_data import PROJECTS


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key and os.environ.get("RENDER"):
        raise RuntimeError("Set SECRET_KEY in the Render environment.")

    app.config.update(
        SECRET_KEY=secret_key or secrets.token_urlsafe(32),
        MAX_CONTENT_LENGTH=16 * 1024,
        WEB3FORMS_ACCESS_KEY=os.environ.get("WEB3FORMS_ACCESS_KEY", ""),
    )

    @app.get("/robots.txt")
    def robots_txt():
        """Tell crawlers the site is public and provide its sitemap URL."""
        sitemap_url = url_for("sitemap_xml", _external=True)
        content = f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n"
        return Response(content, mimetype="text/plain")

    @app.get("/sitemap.xml")
    def sitemap_xml():
        """Publish canonical portfolio pages and project detail URLs."""
        page_urls = "".join(
            f"<url><loc>{url_for(endpoint, _external=True)}</loc></url>"
            for endpoint in ("home", "projects_page", "about_page", "skills_page", "contact_page")
        )
        project_urls = "".join(
            f"<url><loc>{url_for('project_detail', slug=slug, _external=True)}</loc></url>"
            for slug in PROJECTS
        )
        content = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{page_urls}"
            f"{project_urls}"
            "</urlset>"
        )
        return Response(content, mimetype="application/xml")

    @app.get("/projects/<slug>")
    def project_detail(slug):
        """Render a project detail page for a known portfolio project."""
        project = PROJECTS.get(slug)
        if project is None:
            abort(404)
        return render_template("project_detail.html", project=project)

    @app.get("/projects")
    def projects_page():
        """Render the featured projects as a standalone page."""
        return render_template("projects.html")

    @app.get("/about")
    def about_page():
        """Render the profile and education page."""
        return render_template("section_page.html", page_title="About", section_template="_about_section.html", active_page="about")

    @app.get("/skills")
    def skills_page():
        """Render the skills page."""
        return render_template("section_page.html", page_title="Skills", section_template="_skills_section.html", active_page="skills")

    @app.get("/contact")
    def contact_page():
        """Render the contact page."""
        return render_template(
            "section_page.html",
            page_title="Contact",
            section_template="_contact_section.html",
            active_page="contact",
            contact_form=ContactForm(),
            web3forms_access_key=app.config["WEB3FORMS_ACCESS_KEY"],
        )

    @app.get("/")
    def home():
        """Render the portfolio home page."""
        return render_template(
            "index.html",
            contact_form=ContactForm(),
            web3forms_access_key=app.config["WEB3FORMS_ACCESS_KEY"],
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
