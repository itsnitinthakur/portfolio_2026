# portfolio/seed_data.py
"""
The facts loaded by:  python manage.py seed_portfolio

Every fact here comes from the Experience section of Nitin's LinkedIn profile
(linkedin.com/in/nitin-nitin-140a07131), read on 2026-11-14. Nothing else.

Edit this file, then run the command again with --update to push your changes
into the database. Rows are matched on skill name, company, project title and
institution + qualification, so keep one entry per company.

Dates are written "YYYY-MM-DD". LinkedIn gives months only, so every date is the
first of its month; show them as "Jan 2025" in templates (date:"M Y").
"""

import os

NEEDED = None

# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #
PROFILE = {
    "full_name": "Nitin",
    "headline": "Python & Odoo ERP Developer",
    "bio": (
        "I am a Python & Odoo ERP Developer at Kamtronics Technology Pvt. Ltd, where "
        "I build Python automation services and scripts integrated with Django-based "
        "internal tooling, design PostgreSQL database models, and run scheduled "
        "background tasks with Celery and Redis.\n\n"
        "Before that I spent two years at CIBC in Toronto in infrastructure system "
        "integration and automation. Working with the Ansible Tower platform team and "
        "the SQL team, I built an automated workflow for deploying SQL cluster "
        "Availability Groups that cut manual effort and human error by 90%, and new "
        "testing standards that reduced the time to build new workflows by 20%.\n\n"
        "My earlier experience includes a DevOps internship building and deploying a "
        "web application to the cloud, and customer-facing roles at FedEx Ground and "
        "Loblaw in Toronto."
    ),
    "open_to": "",
    "photo_alt": "Portrait of Nitin",
    "location": "",
    "company": "Kamtronics Technology Pvt. Ltd",
    "company_url": "",
    # Kept out of the repository on purpose: set PORTFOLIO_CONTACT_EMAIL in your
    # environment (.env), or type the address into the admin.
    "email": os.environ.get("PORTFOLIO_CONTACT_EMAIL", ""),
    "phone": "",
    "wechat_id": "",
    "github_url": "",
    "linkedin_url": "https://www.linkedin.com/in/nitin-nitin-140a07131/",
}

# --------------------------------------------------------------------------- #
# Skills: the ones LinkedIn lists against each role, plus the tools named in
# the role descriptions (PostgreSQL, Celery, Redis, Ansible, SQL).
# LinkedIn has no proficiency levels, so level is left empty (None).
# Set 1 Familiar, 2 Proficient, 3 Advanced or 4 Expert if you want bars shown.
# --------------------------------------------------------------------------- #
SKILLS = [
    # Backend
    {"name": "Python", "category": "backend", "level": None, "is_featured": True},
    {"name": "Django", "category": "backend", "level": None, "is_featured": True},
    {"name": "Celery", "category": "backend", "level": None, "is_featured": True},
    {"name": "Redis", "category": "backend", "level": None, "is_featured": False},
    {"name": "Application Architecture", "category": "backend", "level": None, "is_featured": False},
    {"name": "Unit Testing", "category": "backend", "level": None, "is_featured": False},
    # Frontend
    {"name": "Web Development", "category": "frontend", "level": None, "is_featured": False},
    {"name": "JavaScript", "category": "frontend", "level": None, "is_featured": False},
    {"name": "HTML Scripting", "category": "frontend", "level": None, "is_featured": False},
    # Databases
    {"name": "PostgreSQL", "category": "database", "level": None, "is_featured": True},
    {"name": "SQL", "category": "database", "level": None, "is_featured": False},
    {"name": "Oracle Database", "category": "database", "level": None, "is_featured": False},
    # DevOps & cloud
    {"name": "Ansible", "category": "devops", "level": None, "is_featured": True},
    {"name": "Cloud Computing", "category": "devops", "level": None, "is_featured": True},
    {"name": "Microsoft Azure", "category": "devops", "level": None, "is_featured": False},
    # ERP & business systems
    {"name": "Odoo", "category": "erp", "level": None, "is_featured": True},
    {"name": "Tally ERP", "category": "erp", "level": None, "is_featured": False},
    # Other
    {"name": "Control Software", "category": "other", "level": None, "is_featured": False},
    {"name": "Agile Project Management", "category": "tools", "level": None, "is_featured": False},
    {"name": "Technical Documentation", "category": "tools", "level": None, "is_featured": False},
    {"name": "Build Strong Relationships", "category": "other", "level": None, "is_featured": False},
    {"name": "Customer Experience", "category": "other", "level": None, "is_featured": False},
    {"name": "Communication", "category": "other", "level": None, "is_featured": False},
]

# --------------------------------------------------------------------------- #
# Experience (all six roles on LinkedIn)
# employment_type: full_time, part_time, contract, internship or freelance.
# end_date None means "current role". Work mode (Remote / Hybrid / On-site) is
# kept in the location line, as LinkedIn shows it.
# --------------------------------------------------------------------------- #
EXPERIENCES = [
    {
        "company": "Kamtronics Technology Pvt. Ltd",
        "job_title": "Python & Odoo ERP Developer",
        "location": "New Delhi, Delhi, India · Remote",
        "employment_type": "freelance",
        "start_date": "2025-01-01",
        "end_date": None,
        "summary": "",
        "highlights": [
            "Developed Python automation services and scripts integrated with "
            "Django-based internal tooling, enhancing operational efficiency.",
            "Designed and maintained PostgreSQL database models and queries, "
            "optimizing data management and retrieval processes.",
            "Built and scheduled asynchronous background tasks using Celery and Redis "
            "for automated health checks and log processing.",
        ],
        "skills": [
            "Python", "Django", "Odoo", "PostgreSQL", "Celery", "Redis",
            "Cloud Computing", "Unit Testing", "Agile Project Management", "Tally ERP",
            "Web Development", "Oracle Database", "HTML Scripting", "Microsoft Azure",
            "Control Software", "JavaScript", "Application Architecture",
        ],
        "is_published": True,
    },
    {
        "company": "CIBC",
        "job_title": "Infrastructure System Integration and Automation",
        "location": "Toronto, Ontario, Canada · Hybrid",
        "employment_type": "full_time",
        "start_date": "2023-01-01",
        "end_date": "2024-12-01",
        "summary": (
            "As an Automation Engineer at CIBC, I analyzed key products and suggested "
            "process improvements on the Ansible platform by implementing best practices "
            "and automating processes. I developed a new workflow with added idempotency "
            "to save time during testing and deployment, which increased deployment "
            "efficiency."
        ),
        "highlights": [
            "Collaborated with the platform team (Ansible Tower) and SQL team to create an "
            "automated workflow for deploying SQL cluster Availability Groups, reducing "
            "manual effort and human error by 90%.",
            "Developed new testing standards before promoting code to production and added "
            "code reusability, reducing the time to create new product and automation "
            "workflows by 20%.",
        ],
        "skills": ["Ansible", "SQL", "Build Strong Relationships", "Technical Documentation"],
        "is_published": True,
    },
    {
        "company": "FedEx Ground",
        "job_title": "Customer Service Representative",
        "location": "Scarborough, Ontario, Canada · On-site",
        "employment_type": "part_time",
        "start_date": "2021-10-01",
        "end_date": "2022-08-01",
        "summary": "",
        "highlights": [
            "Provided customer service by addressing inquiries and resolving issues via "
            "phone, email and chat.",
            "Developed a strong phone presence, ensuring customers felt valued and "
            "understood during interactions.",
            "Self-managed tasks and worked independently in a fast-paced environment.",
        ],
        "skills": ["Customer Experience", "Communication"],
        "is_published": True,
    },
    {
        "company": "Loblaw Companies Limited",
        "job_title": "Operations Assistant",
        "location": "St Clair West, Toronto, Canada",
        "employment_type": "contract",
        "start_date": "2021-10-01",
        "end_date": "2021-11-01",
        "summary": "",
        "highlights": [],
        "skills": ["Communication"],
        "is_published": True,
    },
    {
        "company": "Iha Consulting Services Pvt. Ltd.",
        "job_title": "DevOps Engineer",
        "location": "Hyderabad, Telangana, India",
        "employment_type": "internship",
        "start_date": "2021-06-01",
        "end_date": "2021-07-01",
        "summary": (
            "Developed a web application and user interface for a data science project "
            "and deployed the application to the cloud."
        ),
        "highlights": [],
        "skills": ["Cloud Computing", "Web Development"],
        "is_published": True,
    },
    {
        "company": "UIETH, Panjab University",
        "job_title": "Management",
        "location": "India",
        "employment_type": "part_time",
        "start_date": "2016-09-01",
        "end_date": "2020-01-01",
        "summary": "",
        "highlights": [],
        "skills": ["Unit Testing"],
        "is_published": True,
    },
]

# --------------------------------------------------------------------------- #
# Projects and education: none are listed on the LinkedIn Experience page.
# Add entries here, or in the admin, when you want them on the site.
# --------------------------------------------------------------------------- #
PROJECTS = []

EDUCATION = []
