"""
fallback_jobs.py

The local, curated job list used when live JSearch data isn't available
(no API key, request failure, empty response). This used to be a 12-job
list living in its own jobs.py, then got shrunk to 3 generic "Demo Company"
entries inlined directly inside app.py during the live-API rewiring --
that's a regression worth undoing: app.py should stay thin (routing +
orchestration only), and a 3-job fallback is a much weaker demo experience
than a 12-job one if you're showing this to anyone without live API access
(e.g. during a judged demo with no wifi).
"""

FALLBACK_JOBS = [
    {
        "title": "AI Research Intern",
        "company": "TechLabs",
        "skills": ["Python", "Machine Learning", "Data Analysis", "Git", "SQL"],
    },
    {
        "title": "Data Analyst Intern",
        "company": "DataBridge",
        "skills": ["Python", "SQL", "Excel", "Data Analysis"],
    },
    {
        "title": "Software Engineering Intern",
        "company": "InnovateQ",
        "skills": ["Python", "JavaScript", "Git", "SQL"],
    },
    {
        "title": "Frontend Developer Intern",
        "company": "WebWorks",
        "skills": ["JavaScript", "HTML", "CSS", "React", "Git"],
    },
    {
        "title": "Backend Developer Intern",
        "company": "ServerStack",
        "skills": ["Python", "Flask", "SQL", "Git"],
    },
    {
        "title": "Cloud Computing Intern",
        "company": "CloudNova",
        "skills": ["AWS", "Azure", "Python", "Git"],
    },
    {
        "title": "Cybersecurity Intern",
        "company": "SecureNet",
        "skills": ["Python", "Linux", "Networking", "Security"],
    },
    {
        "title": "UI/UX Design Intern",
        "company": "DesignFlow",
        "skills": ["Figma", "User Research", "UI Design", "Prototyping"],
    },
    {
        "title": "Mobile App Developer Intern",
        "company": "AppForge",
        "skills": ["Swift", "SwiftUI", "Git", "UI Design"],
    },
    {
        "title": "Junior Full Stack Developer",
        "company": "BuildBase",
        "skills": ["HTML", "CSS", "JavaScript", "Python", "SQL", "Git"],
    },
    {
        "title": "AI Systems & Automation Intern",
        "company": "Demo Company",
        "skills": ["Python", "AI", "Automation", "REST API", "Prompt Engineering"],
    },
]
