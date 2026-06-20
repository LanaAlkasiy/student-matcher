import re

from skills import ALL_SKILLS, normalize, to_display


def extract_skills(cv_text):
    """Find which known skills appear in the CV text.

    Returns the skills in their canonical display casing (e.g. "SQL",
    "JavaScript") so they line up exactly with the skill names coming back
    from job postings.
    """
    found_skills = []
    cv_text_lower = cv_text.lower()

    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, cv_text_lower):
            found_skills.append(skill)

    return found_skills


def match_jobs(user_skills, jobs):
    """Score each job against the student's extracted skills.

    Matching is done case-insensitively (via skills.normalize) so a job
    posting that lists "sql" and a CV that lists "SQL" still match -- the
    exact casing a skill happens to be written in shouldn't matter.
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
            "url": job.get("url", "#")
        })

    matched_jobs.sort(key=lambda job: job["match_score"], reverse=True)

    return matched_jobs
