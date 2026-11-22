# Shivnandan Kumar - Developer Portfolio

A personal portfolio project for presenting Shivnandan Kumar's development work, skills, education, and contact information. The site is being built incrementally with Flask and a lightweight frontend.

> **Project status:** The repository contains the Flask foundation, accessible responsive navigation, BloodLink and E-Governance project cards, confirmed About and Education details, categorized skills, and a validated contact form with CSRF and honeypot protection. SEO foundations are in place with Open Graph metadata, an SVG favicon, and dynamic `robots.txt` and `sitemap.xml` routes. BloodLink screenshots are included; the E-Governance screenshot and portfolio deployment remain pending. Local Gmail SMTP delivery has been accepted; production environment configuration remains pending.

## Current Features

- Flask application with an application factory.
- A home route (`/`) that renders a Jinja template.
- Semantic page landmarks and a responsive, icon-based primary navigation dock.
- Narrow-screen layout stacks project cards and compacts the navigation dock and card spacing.
- BloodLink and E-Governance cards with confirmed summaries, technology tags, repository links, and live demos.
- BloodLink card includes responsive, lazy-loaded JPEG screenshots of its public home page and workflow; cropping and compression reduce their combined size by about 71%. The E-Governance card keeps its abstract illustration until a suitable screenshot is available.
- BloodLink stack is labeled as SQLite for local development and Supabase PostgreSQL for production.
- Both project cards link to the supplied live demos.
- About section presents the approved Python & Flask Developer introduction, backend focus, and projects; Education lists the confirmed BCA program, Sai Nath University in Ranchi, and 2026 passing year.
- About uses a compact editorial layout beside a highlighted Education card, then stacks cleanly on phone screens.
- Confirmed skills are grouped into Backend, Frontend, Databases, Developer tools, and Deployment & platform categories.
- Skills use full-width category rows on desktop, adjusted spacing and wrapping on tablets, and stacked labels and tags on phones. Skill badge hover feedback is subtle and disabled for reduced-motion preferences.
- Contact form validates names, email addresses, and message length on the server; CSRF tokens and a hidden honeypot provide basic abuse protection.
- Contact email is sent through configurable SMTP using Python's standard library. SMTP failures are logged with safe stage, exception type, and status-code diagnostics, without logging credentials or message content.
- `smtp_diagnostic.py` checks SMTP connection, TLS, and authentication without sending an email.
- E-Governance artwork remains an abstract CSS illustration; it is not presented as an actual product screenshot.
- A skip link, visible keyboard focus styles, and reduced-motion handling for smooth scrolling.
- Inline SVG navigation icons with accessible names and hover/focus tooltip labels; no icon package is required.
- SEO description and Open Graph metadata, a lightweight SVG favicon, and dynamically generated `robots.txt` and `sitemap.xml` endpoints.
- Pytest checks for the home page, navigation targets, and accessible icon labels.
- Gunicorn included as the planned production WSGI server.

## Technology

- Python and Flask
- HTML templates rendered with Jinja
- Flask-WTF for contact form validation and CSRF protection
- Gunicorn for production serving
- pytest for automated tests

The portfolio site itself does not use a database, authentication, an admin panel, React, Tailwind, PostgreSQL, or SQLAlchemy. BloodLink's database stack belongs to that separate project: SQLite for local development and Supabase PostgreSQL in production.

## Project Structure

```text
.
|-- app.py                 # Flask application factory and routes
|-- email_service.py       # SMTP delivery through Python's standard library
|-- smtp_diagnostic.py     # Safe SMTP/TLS/authentication check; sends no email
|-- forms.py               # Contact form validation and honeypot
|-- requirements.txt       # Runtime dependencies
|-- requirements-dev.txt   # Runtime dependencies plus pytest
|-- static/
|   |-- css/
|   |   `-- styles.css     # Responsive layout and accessibility styles
|   |-- favicon.svg        # Lightweight site icon
|   `-- images/
|       `-- projects/      # Project screenshots
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

Open <http://127.0.0.1:5000> in a browser. The portfolio is still being developed, and sections without confirmed content remain placeholders.

To stop the server, press `Ctrl+C` in the terminal.

## Run Tests

With the virtual environment active, run the test suite from the project root:

```powershell
python -m pytest
```

The current tests check public page content and navigation, responsive CSS, and contact form rendering, input validation, CSRF rejection, honeypot handling, successful mocked delivery, and graceful behavior when SMTP settings are missing. Tests do not send email.

## Application Flow

1. Flask creates the application through `create_app()` in `app.py`.
2. A browser requests `/`.
3. The `home` route renders `templates/index.html`.
4. Flask returns the rendered HTML to the browser. `/robots.txt` and `/sitemap.xml` are generated from the current site host.

The same application object is exposed as `app` for the production server.

## Render Deployment

The planned Render web service can use:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

`app:app` means "load the `app` object from the `app.py` module." Deployment has not been completed yet.

The contact form reads these environment variables. Set them in Render's environment settings; keep credentials out of source control:

- `SECRET_KEY`: a long, random secret used to protect Flask sessions and CSRF tokens. Required on Render.
- `CONTACT_RECIPIENT`: destination inbox for contact messages.
- `SMTP_HOST`: SMTP server hostname from the chosen mail provider.
- `SMTP_PORT`: `587` for STARTTLS or `465` for implicit TLS. Defaults to `587`.
- `SMTP_USERNAME`: SMTP login username.
- `SMTP_PASSWORD`: SMTP password or provider-issued app password.

Until all SMTP values are set, the form validates submissions but reports that delivery is unavailable. The recipient address is kept in environment configuration and is not rendered on the page.

To diagnose SMTP locally without sending a message, set the SMTP environment variables in the same terminal session and run:

```powershell
python .\smtp_diagnostic.py
```

The diagnostic prints only stage results, exception types, and numeric SMTP status codes when available. It never prints passwords, message content, or exception messages.

## Roadmap

Development follows the approved product requirements and proceeds in small reviewed steps:

- Add an E-Governance screenshot when the project can be captured, and create a social sharing image.
- Refine visual details across the portfolio as sections are reviewed.
- Create the responsive visual design and accessible interactions.
- Add image optimization and lazy loading for project imagery.
- Configure SMTP credentials in Render and verify an actual delivery.
- Configure and verify Render deployment.

Personal details, project URLs, assets, and email credentials will be added only after they are confirmed. Version 1.0 does not include a database, admin panel, or authentication system.

## GitHub

Source repository: <https://github.com/shivnandan-kumar/shivnandan-portfolio>
