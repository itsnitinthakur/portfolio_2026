# portfolio/seed_data.py
"""
The facts loaded by:  python manage.py seed_portfolio

Sources, all read on 2026-11-14:
  - Experience and Education: Nitin's LinkedIn profile (linkedin.com/in/nitin-nitin-140a07131)
  - Projects: his GitHub repositories (github.com/itsnitinthakur)
  - Company and products: the Kamtronics website (www.kamtronics.com)

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
        "Loblaw in Toronto.\n\n"
        "Today I represent Kamtronics, a New Delhi manufacturer of ultrasonic welding "
        "and cutting machines, non-woven bag making machines, flexo printing machines "
        "and induction heating systems. If you need one of these machines, or you "
        "supply machinery, automation or components and want a partner in India, "
        "please get in touch."
    ),
    "open_to": "Machine enquiries from customers, and partnerships with machinery and automation suppliers",
    "photo_alt": "Portrait of Nitin",
    "location": "New Delhi, India",
    "company": "Kamtronics Technology Pvt. Ltd",
    "company_url": "https://www.kamtronics.com",
    # Kept out of the repository on purpose: set PORTFOLIO_CONTACT_EMAIL in your
    # environment (.env), or type the address into the admin.
    "email": os.environ.get("PORTFOLIO_CONTACT_EMAIL", ""),
    "phone": "",
    "wechat_id": "",
    "github_url": "https://github.com/itsnitinthakur",
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
    # Computer vision & hardware (from the GitHub projects)
    {"name": "Computer Vision", "category": "vision", "level": None, "is_featured": True},
    {"name": "OpenCV", "category": "vision", "level": None, "is_featured": False},
    {"name": "Machine Vision", "category": "vision", "level": None, "is_featured": True},
    {"name": "YOLO (Ultralytics)", "category": "vision", "level": None, "is_featured": False},
    {"name": "Raspberry Pi", "category": "vision", "level": None, "is_featured": False},
    {"name": "Flask", "category": "backend", "level": None, "is_featured": False},
    {"name": "Docker", "category": "devops", "level": None, "is_featured": False},
    # Other
    {"name": "Scrum", "category": "tools", "level": None, "is_featured": False},
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
# Projects (shown in this order), from github.com/itsnitinthakur
# status: completed, in_progress, live or archived.
# "company" links the project to the experience entry with that company name.
# "cover_image" is a file in portfolio/seed_assets/, attached on first load.
# --------------------------------------------------------------------------- #
PROJECTS = [
    {
        "title": "Dock Counter: CCTV Counting for Loading and Unloading",
        "summary": (
            "Counts cartons, bags and paper rolls going in and out of a factory dock "
            "from CCTV video, and checks the count against the Odoo receipt or delivery."
        ),
        "description": (
            "The problem\n"
            "Goods loaded into and unloaded from trucks are counted by hand, and the "
            "numbers are then typed into Odoo. Mistakes and missing items are found late.\n\n"
            "What I built\n"
            "A Python tool that reads a video file or a live CCTV stream (it works with "
            "CP Plus cameras over RTSP), detects and tracks each item with a YOLO model, "
            "and counts it once as it crosses a line or lands in a zone. It can find boxes "
            "or rolls from a text description with no training, or use a model trained on "
            "the factory's own footage. Every run saves a photo and a CSV row per item. "
            "A separate script compares the count with the expected quantity on the Odoo "
            "receipt or delivery and posts a note with photos, for example \"Expected 200, "
            "Counted 196, Difference -4\". It never validates the transfer itself: a "
            "storekeeper confirms.\n\n"
            "Where it stands\n"
            "In progress. It is being tested on real loading footage from the factory "
            "cameras, and the plan is to check it against hand counts on 10 real truck "
            "loads before trusting it for receipts."
        ),
        "impact": "",
        "role": "Design and development",
        "company": "Kamtronics Technology Pvt. Ltd",
        "skills": ["Python", "Computer Vision", "YOLO (Ultralytics)", "OpenCV", "Odoo", "Unit Testing"],
        "status": "in_progress",
        "github_url": "https://github.com/itsnitinthakur/dock-counter",
        "live_url": "",
        "cover_image": "dock-counter.jpg",
        "cover_image_alt": (
            "CCTV frame of a truck being loaded at the factory dock, with each detected "
            "carton outlined and a box marked as counted in"
        ),
        "is_featured": True,
        "is_published": True,
    },
    {
        "title": "Lighter Vision Kit: Rebuilding a Factory Inspection Machine with Open-Source Tools",
        "summary": (
            "Reverse-engineered a two-camera lighter pick-up machine and rebuilt its "
            "vision software with free tools: it finds each lighter at any angle, tells "
            "front from back, rejects defects and gives the robot a grab point in mm."
        ),
        "description": (
            "The problem\n"
            "A lighter production line uses a Chinese vision machine: two industrial cameras "
            "over a white backlight find each lighter on the belt so a robot can pick it up. "
            "Its software is closed and licence-locked, and there is no documentation, so "
            "the factory cannot change, repair or copy it.\n\n"
            "What I built\n"
            "First, tools that read the machine without changing it: a scanner that reports "
            "the software, versions and settings in a copied machine folder, a PowerShell "
            "collector for the machine PC, and a converter that turns the maker's recipe "
            "files into open JSON recipes. Then a free replacement in Python and OpenCV: it "
            "learns a lighter's outline from one good image, matches it at any angle, tells "
            "front from back, checks for defects (missing wheel, missing hood, chipped body, "
            "missing lever), and converts the grab point from pixels to millimetres for the "
            "robot. Because shop photos are copyrighted and wrongly lit, a generator makes "
            "realistic backlit images of the lighter types sold in India for testing.\n\n"
            "Results\n"
            "On a 200-lighter test set: every lighter accepted or rejected correctly, front "
            "and back always right, worst angle error 0.10 degrees. Two Jupyter notebooks "
            "show every step as pictures, and 19 automated tests cover the pipeline.\n\n"
            "Where it stands\n"
            "In progress. Next: real images and the lens focal length from the factory to "
            "set the true mm-per-pixel, and the PLC register map before connecting to the "
            "live machine."
        ),
        "impact": "",
        "role": "Reverse engineering, design and development",
        "company": "Kamtronics Technology Pvt. Ltd",
        "skills": ["Python", "Computer Vision", "Machine Vision", "OpenCV", "Unit Testing"],
        "status": "in_progress",
        "github_url": "https://github.com/itsnitinthakur/lighter_vision_kit",
        "live_url": "",
        "cover_image": "lighter-vision-kit.jpg",
        "cover_image_alt": (
            "Three backlit lighter images: two outlined green as OK with angle and side, "
            "one outlined red as rejected for a missing wheel"
        ),
        "is_featured": True,
        "is_published": True,
    },
    {
        "title": "QR Code Attendance System for Raspberry Pi",
        "summary": (
            "Staff clock in and out by scanning a QR code on a kiosk screen with their "
            "phone. Built to run on a Raspberry Pi 3 Model B+."
        ),
        "description": (
            "The problem\n"
            "A small office needs attendance records without buying a biometric machine "
            "or a paid app.\n\n"
            "What I built\n"
            "A lightweight Flask web app with three screens. A kiosk screen shows a QR "
            "code that refreshes automatically and carries a short-lived token, so a "
            "photo of an old code cannot be reused. Staff scan it with their phone, enter "
            "their employee ID and choose In or Out. An admin page lists every record, "
            "newest first. Employees are kept in a JSON file and attendance in a CSV file, "
            "so there is no database to install.\n\n"
            "Where it stands\n"
            "Version 1.0 is complete. It runs on a PC for testing and is designed for a "
            "Raspberry Pi 3 Model B+."
        ),
        "impact": "",
        "role": "Design and development",
        "company": None,
        "skills": ["Python", "Flask", "Raspberry Pi"],
        "status": "completed",
        "github_url": "https://github.com/itsnitinthakur/attendance_raspberry",
        "live_url": "",
        "cover_image": "attendance-raspberry.jpg",
        "cover_image_alt": "Kiosk screen showing a QR code to scan to clock in or out",
        "is_featured": True,
        "is_published": True,
    },
    {
        "title": "Odoo 18 Development Environment",
        "summary": (
            "A local setup for building and debugging custom Odoo 18 modules, with "
            "PostgreSQL and VS Code debugging."
        ),
        "description": (
            "What it is\n"
            "My working environment for Odoo development: Odoo 18 run from source with "
            "its own configuration, a separate folder for custom modules, a PostgreSQL "
            "database, and a VS Code launch configuration so Odoo can be started and "
            "stepped through in the debugger. A Docker Compose file with PostgreSQL 15 "
            "is included as an alternative way to start Odoo in containers.\n\n"
            "Why it matters\n"
            "Custom modules and integrations, such as the Dock Counter's Odoo connection, "
            "are built and tested here against a test database before anything touches "
            "the live system."
        ),
        "impact": "",
        "role": "Setup and configuration",
        "company": "Kamtronics Technology Pvt. Ltd",
        "skills": ["Odoo", "Python", "PostgreSQL", "Docker"],
        "status": "in_progress",
        "github_url": "https://github.com/itsnitinthakur/odoo18",
        "live_url": "",
        "cover_image": "",
        "cover_image_alt": "",
        "is_featured": False,
        "is_published": True,
    },
]

# --------------------------------------------------------------------------- #
# Education (shown in this order), from LinkedIn
# --------------------------------------------------------------------------- #
EDUCATION = [
    {
        "institution": "Lambton College",
        "qualification": "Postgraduate Degree",
        "field_of_study": "Computer Software and Database Development",
        "location": "Canada",
        "start_year": 2021,
        "end_year": 2023,
        "honours": "GPA 3.54",
        "description": (
            "Front-end and back-end development and program logic, applied by building "
            "projects in a team. Activities: social justice, basketball."
        ),
        "is_published": True,
    },
    {
        "institution": "UIETH, Panjab University",
        "qualification": "Bachelor of Engineering (BE)",
        "field_of_study": "Electronics and Communications Engineering",
        "location": "India",
        "start_year": 2016,
        "end_year": 2020,
        "honours": "",
        "description": "",
        "is_published": True,
    },
]

# --------------------------------------------------------------------------- #
# Company, from www.kamtronics.com
# --------------------------------------------------------------------------- #
COMPANY = {
    "name": "Kamtronics Technology Pvt. Ltd",
    "tagline": "Ultrasonic machines, bag making machines and induction heating systems, made in India",
    "description": (
        "Kamtronics manufactures and supplies ultrasonic machines in India: ultrasonic "
        "welding, sewing and cutting machines, non-woven bag making machines, flexo "
        "printing machines, induction heating systems, and ultrasonic components such "
        "as generator boxes, boosters and horns. The company was previously known as "
        "Unitech Allied Automation.\n\n"
        "It has also installed induction heating systems on extruders and injection "
        "moulding machines in place of conventional band heaters. Every machine goes "
        "through quality checks by the in-house team of engineers and technicians "
        "before it ships.\n\n"
        "Kamtronics is growing beyond India and wants to work with companies in other "
        "countries on technology, production and quality."
    ),
    "website": "https://www.kamtronics.com",
    "established_year": 2013,
    "staff_count": 50,
    "engineer_count": 10,
    "unit_count": 2,
    # The website names ISO 9001:2008, a version of the standard that was withdrawn
    # in 2018. Fill this in only with a certificate that is current.
    "certifications": "",
    "capabilities": [
        "Manufacture and supply of ultrasonic machines",
        "Non-woven bag making and flexo printing machines",
        "Induction heating retrofits for extruders and injection moulding machines",
        "In-house quality testing by experienced engineers",
        "Spare ultrasonic generator boxes, boosters and horns",
    ],
    "clients": [
        "IIT Delhi",
        "IIT Roorkee",
        "Avery Dennison",
        "UFLEX",
        "Kurl-On",
        "BKT",
        "Thermo King",
        "Elentec",
        "TS Tech",
        "Asbah",
        "SGM",
        "Deco",
    ],
    "offices": [
        "Corporate office: A-6, Plot No. 14 & 15, DLF Industrial Area, behind Moti Nagar Metro Station, New Delhi 110015",
        "Office: Plot No. 31-32, Shreeji Industrial Estate, Raipur Mill Compound, Saraspur, Ahmedabad, Gujarat 380018",
    ],
    "sales_email": "sales@kamtronics.com",
    "sales_phone": "+91 97116 23990",
}

# --------------------------------------------------------------------------- #
# Products, from www.kamtronics.com ("We Offer" and the featured machines)
# category: welding, cutting, bag_making, printing, induction, cleaning, components
# --------------------------------------------------------------------------- #
PRODUCTS_URL = "https://www.kamtronics.com/products.html"

PRODUCTS = [
    # Bag making
    {"name": "D-Cut Non Woven Bag Making Machine", "category": "bag_making", "is_featured": True,
     "summary": "Makes non-woven bags in many sizes, with D-cut, U-cut and T-shirt cut styles."},
    {"name": "Non Woven Box Bag Making Machine with Online Loop Handle", "category": "bag_making", "is_featured": True,
     "summary": "Turns non-woven fabric into box bags of different sizes, with the loop handle attached in line."},
    {"name": "Automatic Non-Woven Fabric Bag Making Machine with Online Loop Handle", "category": "bag_making", "is_featured": False,
     "summary": "Fully automatic non-woven bag production with in-line loop handle fixing."},
    {"name": "Ultrasonic Non Woven Bag Making Machine", "category": "bag_making"},
    {"name": "Ultrasonic Loop Handle Machine", "category": "bag_making"},
    {"name": "Ultrasonic Mask Making Machine", "category": "bag_making"},
    {"name": "Ultrasonic Corrugated Box Making Machine", "category": "bag_making"},
    # Printing
    {"name": "Two Color Flexo Printing Machine", "category": "printing", "is_featured": True,
     "summary": "Two-colour flexographic printing, designed for packaging."},
    # Welding
    {"name": "Ultrasonic Plastic Welding Machine", "category": "welding", "is_featured": True,
     "summary": "Joins thermoplastic parts with ultrasonic vibration, without glue, screws or heat elements."},
    {"name": "Ultrasonic Welding Machine", "category": "welding"},
    {"name": "Ultrasonic Hand Gun", "category": "welding"},
    {"name": "Ultrasonic Punch Welding Machine", "category": "welding"},
    {"name": "Ultrasonic Paper Cup Welding Machine", "category": "welding"},
    {"name": "Spin Welding Machine", "category": "welding"},
    {"name": "Tube Sealing Machine", "category": "welding"},
    # Cutting and sewing
    {"name": "Ultrasonic Sewing Machine", "category": "cutting"},
    {"name": "Ultrasonic Label Cutting Machine", "category": "cutting"},
    {"name": "Ultrasonic Fabric Cutter", "category": "cutting"},
    {"name": "Ultrasonic Food Cutter", "category": "cutting"},
    {"name": "Ultrasonic Rubber Cutter for Tyre Industries", "category": "cutting"},
    {"name": "Ultrasonic Cut & Fold Machine", "category": "cutting"},
    # Induction heating
    {"name": "Induction Heating Machine", "category": "induction", "is_featured": True,
     "summary": "Induction heating, including retrofits on extruders and injection moulding machines in place of band heaters."},
    {"name": "Induction Heating System for Boilers", "category": "induction"},
    # Cleaning, drilling and other
    {"name": "Ultrasonic Cleaning Machine", "category": "cleaning"},
    {"name": "Ultrasonic Drill Machine", "category": "cleaning"},
    {"name": "Ultrasonic Humidifier", "category": "cleaning"},
    # Components
    {"name": "Ultrasonic Generator Box", "category": "components"},
    {"name": "Ultrasonic Booster", "category": "components"},
    {"name": "Ultrasonic Horns", "category": "components"},
]
