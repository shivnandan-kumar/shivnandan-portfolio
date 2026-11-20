# Shivnandan Kumar - Developer Portfolio

A personal portfolio project for presenting Shivnandan Kumar's development work, skills, education, and contact information. The site is being built incrementally with Flask and a lightweight frontend.

> **Project status:** The repository currently contains the initial Flask foundation and a basic home page. Portfolio sections, final design, contact form, SEO assets, and production deployment are planned but are not implemented yet.

## Current Features

- Flask application with an application factory.
- A home route (`/`) that renders a Jinja template.
- A basic pytest check for the home page response.
- Gunicorn included as the planned production WSGI server.

## Technology

- Python and Flask
- HTML templates rendered with Jinja
- Flask-WTF, reserved for form validation and CSRF protection when the contact form is implemented
- Gunicorn for production serving
- pytest for automated tests

The project does not use a database, authentication, an admin panel, React, Tailwind, PostgreSQL, or SQLAlchemy.

## Project Structure

```text
.
|-- app.py                 # Flask application factory and routes
|-- requirements.txt       # Runtime dependencies
|-- requirements-dev.txt   # Runtime dependencies plus pytest
|-- templates/
|   `-- index.html         # Home page template
`-- tests/
    `-- test_routes.py     # Tests for public Flask routes
```

## Requirements

- Python 3.9 or newer
- pip

## Run Locally (Windows PowerShell)

Open PowerShell in the project directory and create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly instead of changing the system execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Install the development dependencies (this also installs the runtime dependencies):

```powershell
python -m pip install -r requirements-dev.txt
```

Start the Flask development server:

```powershell
python -m flask --app app run
```

Open <http://127.0.0.1:5000> in a browser. The current page is a placeholder while the portfolio is developed.

To stop the server, press `Ctrl+C` in the terminal.

## Run Tests

With the virtual environment active, run the test suite from the project root:

```powershell
python -m pytest
```

The current test checks that `GET /` returns HTTP `200` and includes the expected home-page heading.

## Application Flow

1. Flask creates the application through `create_app()` in `app.py`.
2. A browser requests `/`.
3. The `home` route renders `templates/index.html`.
4. Flask returns the rendered HTML to the browser.

The same application object is exposed as `app` for the production server.

## Render Deployment

The planned Render web service can use:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

`app:app` means "load the `app` object from the `app.py` module." Deployment has not been completed yet. The current app does not require environment variables; production secrets and email settings will be documented when those features are implemented.

## Roadmap

Development follows the approved product requirements and proceeds in small reviewed steps:

- Build the semantic page structure and navigation.
- Add approved personal content, projects, education, and skills.
- Create the responsive visual design and accessible interactions.
- Add image optimization, favicon, Open Graph metadata, `sitemap.xml`, and `robots.txt`.
- Implement the contact form with server-side validation, spam protection, and email delivery.
- Add tests for form validation and relevant routes.
- Configure and verify Render deployment.

Personal details, project URLs, assets, and email credentials will be added only after they are confirmed. Version 1.0 does not include a database, admin panel, or authentication system.

## GitHub

Source repository: <https://github.com/shivnandan-kumar/shivnandan-portfolio>
