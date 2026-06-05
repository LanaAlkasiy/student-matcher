def get_real_jobs(user_skills):
    """
    Temporary real-jobs connector.
    Later this will call Adzuna/JSearch API.
    For now, it returns jobs in the same format your matcher expects.
    """

    search_terms = user_skills[:3] if user_skills else ["Python", "Data Analysis"]

    jobs = [
        {
            "title": f"{search_terms[0]} Intern",
            "company": "Live Job Source",
            "skills": search_terms + ["SQL", "Excel"]
        },
        {
            "title": "Junior Data Analyst",
            "company": "Remote Hiring Partner",
            "skills": ["Python", "SQL", "Excel", "Data Analysis"]
        },
        {
            "title": "Software Engineering Intern",
            "company": "Tech Startup",
            "skills": ["Python", "JavaScript", "Git", "React"]
        }
    ]

    return jobs