"""Flask application entry point for the portfolio."""

import os
import secrets

from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for

from email_service import ContactDeliveryError, send_contact_message
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
        CONTACT_RECIPIENT=os.environ.get("CONTACT_RECIPIENT", ""),
        SMTP_HOST=os.environ.get("SMTP_HOST", ""),
        SMTP_PORT=int(os.environ.get("SMTP_PORT", "587")),
        SMTP_USERNAME=os.environ.get("SMTP_USERNAME", ""),
        SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD", ""),
    )

    @app.get("/robots.txt")
    def robots_txt():
        """Tell crawlers the site is public and provide its sitemap URL."""
        sitemap_url = url_for("sitemap_xml", _external=True)
        content = f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n"
        return Response(content, mimetype="text/plain")

    @app.get("/sitemap.xml")
    def sitemap_xml():
        """Publish canonical portfolio and project detail URLs."""
        page_url = url_for("home", _external=True)
        project_urls = "".join(
            f"<url><loc>{url_for('project_detail', slug=slug, _external=True)}</loc></url>"
            for slug in PROJECTS
        )
        content = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{page_url}</loc></url>"
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

    @app.route("/", methods=["GET", "POST"])
    def home():
        """Render the portfolio home page."""
        contact_form = ContactForm()

        if request.method == "POST":
            if contact_form.website.data:
                return redirect(url_for("home", _anchor="contact"))

            if contact_form.validate_on_submit():
                try:
                    send_contact_message(
                        name=contact_form.name.data,
                        sender_email=contact_form.email.data,
                        message=contact_form.message.data,
                        config=app.config,
                    )
                except ContactDeliveryError as error:
                    app.logger.error(
                        "Contact form returned HTTP 503 (exception_type=%s)",
                        type(error).__name__,
                    )
                    flash(
                        "Your message could not be sent right now. Please try again later.",
                        "error",
                    )
                    return render_template("index.html", contact_form=contact_form), 503

                flash("Thanks for reaching out. Your message has been sent.", "success")
                return redirect(url_for("home", _anchor="contact"))

            return render_template("index.html", contact_form=contact_form), 400

        return render_template("index.html", contact_form=contact_form)

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
