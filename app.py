"""Flask application entry point for the portfolio."""

from flask import Flask, render_template


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.get("/")
    def home():
        """Render the portfolio home page."""
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
