# Shivnandan Kumar - Developer Portfolio

A personal portfolio project for presenting Shivnandan Kumar's development work, skills, education, and contact information. The site is being built incrementally with Flask and a lightweight frontend.

> **Project status:** The portfolio includes responsive case-study pages for BloodLink and E-Governance, confirmed About and Education details, categorized skills, and a client-side Web3Forms contact form with required-field validation and a honeypot. SEO foundations include Open Graph metadata, an SVG favicon, and dynamic `robots.txt` and `sitemap.xml` routes. The Render Blueprint is prepared; Render setup and testing the contact form on the live domain remain manual steps. BloodLink screenshots are included; E-Governance screenshots are not available in its repository.

## Current Features

- Flask application with an application factory.
- Dedicated top-level routes for Home (`/`), Projects (`/projects`), About (`/about`), Skills (`/skills`), and Contact (`/contact`). Each navigation icon opens its page at the top.
- Semantic page landmarks and a responsive, icon-based primary navigation dock.
- A warm near-black and brown portfolio theme with restrained copper accents, a white-framed red portrait, high-impact two-line developer headline, centered icon navigation, and responsive confirmed profile copy.
- Narrow-screen layout stacks project cards and compacts the navigation dock and card spacing.
- Mobile navigation uses a smaller dock, icons, and tighter header spacing; section spacing is reduced for a more balanced page flow.
- BloodLink and E-Governance cards with confirmed summaries, technology tags, repository links, and live demos.
- Dedicated `/projects/bloodlink` and `/projects/egovernance` case-study pages with feature descriptions and technology lists extracted from each project's public README.
- BloodLink card includes responsive, lazy-loaded JPEG screenshots of its public home page and workflow; cropping and compression reduce their combined size by about 71%. The E-Governance card keeps its abstract illustration until a suitable screenshot is available.
- Footer links to the GitHub and LinkedIn profiles listed in the public project repository.
- Hero displays the confirmed “Open to work” status and provides a downloadable resume PDF.
- BloodLink stack is labeled as SQLite for local development and Supabase PostgreSQL for production.
- Both project cards link to the supplied live demos.
- About section presents the approved Python & Flask Developer introduction, backend focus, and projects; Education lists the confirmed BCA program, Sai Nath University in Ranchi, and 2026 passing year.
- About uses a compact editorial layout beside a highlighted Education card, then stacks cleanly on phone screens.
- Confirmed skills are grouped into Backend, Frontend, Databases, Developer tools, and Deployment & platform categories.
- Skills use full-width category rows on desktop, adjusted spacing and wrapping on tablets, and stacked labels and tags on phones. Skill badge hover feedback is subtle and disabled for reduced-motion preferences.
- Contact form sends validated browser submissions to Web3Forms using JSON `fetch`, with required fields, length limits, a loading state, and the existing hidden honeypot.
- The Web3Forms Access Key is rendered into client-side HTML and is therefore public by design. It is never stored in Git; configure it through `WEB3FORMS_ACCESS_KEY`.
- Direct browser submissions do not pass through Flask-WTF validation or CSRF protection. Browser validation and the honeypot improve the experience and filter basic bots, but client-side checks can be bypassed.
- `email_service.py` and `smtp_diagnostic.py` remain as legacy SMTP implementation and no-email diagnostic; they are no longer called by the production contact flow.
- E-Governance artwork remains an abstract CSS illustration; it is not presented as an actual product screenshot.
- A skip link, visible keyboard focus styles, and direct page navigation through the icon dock.
- Inline SVG navigation icons with accessible names and hover/focus tooltip labels; no icon package is required.
- SEO description and Open Graph metadata, a lightweight SVG favicon, and dynamically generated `robots.txt` and `sitemap.xml` endpoints.
- Open Graph and large-image social preview metadata use the portfolio portrait and project screenshots already available in the repository.
- Pytest checks for the home page, navigation targets, and accessible icon labels.
- Gunicorn configured as the production WSGI server for Render.

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
|-- project_data.py        # Confirmed project case-study content
|-- render.yaml            # Render web service and environment variable blueprint
|-- .env.example           # Placeholder environment variable names only
|-- email_service.py       # Legacy SMTP delivery code, not used by production contact flow
|-- smtp_diagnostic.py     # Legacy safe SMTP/TLS/authentication check; sends no email
|-- forms.py               # Contact field rendering and honeypot definition
|-- requirements.txt       # Runtime dependencies
|-- requirements-dev.txt   # Runtime dependencies plus pytest
|-- static/
|   |-- documents/
|   |   `-- shivnandan-kumar-resume.pdf # Downloadable resume
|   |-- css/
|   |   `-- styles.css     # Responsive layout and accessibility styles
|   |-- js/
|   |   `-- contact-form.js # Client-side validation and Web3Forms submission
|   |-- favicon.svg        # Lightweight site icon
|   `-- images/
|       `-- projects/      # Project screenshots
|-- templates/
|   |-- index.html         # Home page template
|   |-- projects.html      # Projects landing page
|   |-- section_page.html  # Shared About, Skills, and Contact page shell
|   |-- _site_header.html  # Shared accessible navigation dock
|   |-- _projects_section.html # Shared project listing
|   |-- _about_section.html    # About and education content
|   |-- _skills_section.html   # Skills content
|   |-- _contact_section.html  # Web3Forms contact form
|   `-- project_detail.html # Shared case-study page template
`-- tests/
    `-- test_routes.py     # Public-route and contact integration contract tests
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

Open <http://127.0.0.1:5000> in a browser. The project case studies are available at `/projects/bloodlink` and `/projects/egovernance`.

To stop the server, press `Ctrl+C` in the terminal.

## Run Tests

With the virtual environment active, run the test suite from the project root:

```powershell
python -m pytest
```

The current tests check public page content and navigation, responsive CSS, contact-form markup, the Flask route/CSRF boundary, and key client-script behavior contracts. The browser-side test is a source contract check; it does not call Web3Forms or send a real message. The legacy SMTP unit test uses a mock server.

## Application Flow

1. Flask creates the application through `create_app()` in `app.py`.
2. A browser requests `/`.
3. The `home` route renders `templates/index.html`; `/projects/<slug>` renders a known project case study.
4. Flask returns the rendered HTML to the browser. `/robots.txt` and `/sitemap.xml` are generated from the current site host and include the project case studies.

The same application object is exposed as `app` for the production server.

## Render Deployment

The repository includes a `render.yaml` Blueprint for the Flask web service:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

`app:app` means "load the `app` object from the `app.py` module." The Blueprint generates `SECRET_KEY` and requests `WEB3FORMS_ACCESS_KEY` without putting the key in source control.

The portfolio sends contact submissions from the visitor's browser to Web3Forms, so its production contact flow does not use Gmail SMTP. The Access Key is public in the rendered form, as expected for Web3Forms client-side integration. Configure it in Render's environment settings and never commit a real key.

To create the service:

1. Sign in to Render and choose **New → Blueprint**.
2. Connect `shivnandan-kumar/shivnandan-portfolio` and select the branch containing `render.yaml`.
3. Review the proposed web service and provide `WEB3FORMS_ACCESS_KEY` in Render's environment settings. Do not paste the key into chat or Git.
4. Create the Blueprint and wait for the first deploy to finish.
5. Open the generated `onrender.com` URL and check the home page and project pages. Test contact submission only after Web3Forms has approved the domain, if approval is required.

Do not paste the Access Key into chat or commit it to Git. Render Blueprint creation and the final live smoke-check require access to your Render account and are not performed by a repository push.

The application reads these environment variables:

- `SECRET_KEY`: a long, random secret used to protect Flask sessions and CSRF tokens. Required on Render.
- `WEB3FORMS_ACCESS_KEY`: your Web3Forms access key. The key is included in rendered client-side form markup and is public; it is not an application secret. Use the placeholder in `.env.example` only as a setup guide, then configure the real key in your local environment or Render dashboard.

Use `.env.example` as a variable-name reference and set `WEB3FORMS_ACCESS_KEY` in your shell or local launcher before starting Flask; the application does not load `.env` files automatically. Flask-WTF's CSRF token is not submitted: the browser sends directly to Web3Forms instead of posting to Flask. This means Flask-WTF does not validate or protect this contact submission; client-side validation is bypassable.

Web3Forms documents that some platform-provided free subdomains may not be approved; a custom domain may be required. Render's free `onrender.com` hostname has not been tested for this portfolio, so successful Web3Forms delivery there is not confirmed. Check Web3Forms domain approval and test the deployed form before relying on it.

The legacy SMTP diagnostic can still be used locally without sending a message if you separately configure SMTP values:

```powershell
python .\smtp_diagnostic.py
```

The diagnostic prints only stage results, exception types, and numeric SMTP status codes when available. It never prints passwords, message content, or exception messages.

## Roadmap

Development follows the approved product requirements and proceeds in small reviewed steps:

- Add an E-Governance screenshot when the project can be captured.
- Refine visual details across the portfolio as sections are reviewed.
- Create the responsive visual design and accessible interactions.
- Add image optimization and lazy loading for project imagery.
- Test Web3Forms submission from the deployed Render domain after any required domain approval.
- Configure and verify Render deployment.

Personal details, project URLs, assets, and email credentials will be added only after they are confirmed. Version 1.0 does not include a database, admin panel, or authentication system.

## GitHub

Source repository: <https://github.com/shivnandan-kumar/shivnandan-portfolio>
