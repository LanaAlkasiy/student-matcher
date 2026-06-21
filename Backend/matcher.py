from skills import find_skills_in_text, normalize, to_display


def extract_skills(cv_text):
    """Find which known skills (and synonyms) appear in the CV text.

    Returns canonical display-cased names (e.g. "SQL", "Machine Learning")
    so they line up exactly with the skill names coming back from job
    postings. The actual scanning logic now lives in skills.py so CVs and
    job descriptions are always parsed the same way.
    """
    return find_skills_in_text(cv_text)


def match_jobs(user_skills, jobs):
    """Score each job against the student's extracted skills.

    Matching is case-insensitive (via skills.normalize) so a job posting
    that lists "sql" and a CV that lists "SQL" still match -- the exact
    casing a skill happens to be written in shouldn't matter.
    """
    user_skills_normalized = {normalize(s) for s in user_skills}

    matched_jobs = []

    for job in jobs:
        required_skills = job["skills"]

        matched_skills = []
        missing_skills = []

        for skill in required_skills:
            if normalize(skill) in user_skills_normalized:
                matched_skills.append(to_display(skill))
            else:
                missing_skills.append(to_display(skill))

        match_score = (
            int((len(matched_skills) / len(required_skills)) * 100)
            if required_skills
            else 0
        )

        matched_jobs.append({
            "title": job["title"],
            "company": job["company"],
            "match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "url": job.get("url", "#"),
            "employment_type": job.get("employment_type", "Internship"),
            "location": job.get("location", "Remote"),
        })

    matched_jobs.sort(key=lambda job: job["match_score"], reverse=True)

    return matched_jobs
