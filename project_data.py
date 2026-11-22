"""Confirmed portfolio project details sourced from their public repositories."""

PROJECTS = {
    "bloodlink": {
        "slug": "bloodlink",
        "title": "BloodLink",
        "category": "Donor matching and verification",
        "summary": (
            "A Flask donor network for verified blood requests, local donor matching, "
            "and donation follow-through."
        ),
        "overview": (
            "BloodLink brings donor and requester workflows together. Donors can submit "
            "profiles for review, while requesters can create blood requests and follow "
            "their progress. Matching checks blood group and pincode first, then expands "
            "to donors in the same city."
        ),
        "features": [
            "Donor and requester accounts with email OTP verification.",
            "Admin review of donor profiles and blood requests.",
            "Pincode-first matching with a city fallback.",
            "Notifications and an invitation-to-confirmation donation workflow.",
            "PDF certificates after completed donations are confirmed.",
        ],
        "technologies": [
            "Python",
            "Flask",
            "SQLite (local development)",
            "Supabase PostgreSQL (production)",
            "Bootstrap 5",
            "ReportLab",
        ],
        "repository": "https://github.com/shivnandan-kumar/bloodlink-flask",
        "demo": "https://bloodlink-flask.onrender.com/",
        "screenshots": [
            {
                "src": "images/projects/bloodlink-home.jpg",
                "alt": "BloodLink home page showing its donor network overview.",
                "caption": "BloodLink home page",
            },
            {
                "src": "images/projects/bloodlink-how-it-works.jpg",
                "alt": "BloodLink workflow showing detail submission, admin verification, and local matching.",
                "caption": "Request verification and local matching workflow",
            },
        ],
    },
    "egovernance": {
        "slug": "egovernance",
        "title": "E-Governance Complaint and Service Management Portal",
        "category": "Civic services",
        "summary": (
            "A citizen complaint workflow for submitting issues, receiving reference "
            "numbers, and tracking resolution."
        ),
        "overview": (
            "The portal supports a complaint lifecycle from citizen submission through "
            "administrator review and status updates. Citizens can follow complaint "
            "history and submit feedback, while administrators manage complaints and "
            "review service activity."
        ),
        "features": [
            "Citizen registration and secure account login.",
            "Complaint submission with supporting documents and a reference number.",
            "Complaint status tracking and history timeline.",
            "Administrator search, filtering, status updates, and user management.",
            "Feedback monitoring, analytics, and CSV/Excel export.",
        ],
        "technologies": [
            "Python",
            "Flask",
            "Supabase PostgreSQL",
            "HTML, CSS, JavaScript",
            "Chart.js",
            "Render",
        ],
        "repository": "https://github.com/shivnandan-kumar/egovportal",
        "demo": "https://egovportal-6lpv.onrender.com",
        "screenshots": [],
    },
}
