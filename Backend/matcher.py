import re

def extract_skills(cv_text):
    skills_list = [
        "python",
        "java",
        "javascript",
        "html",
        "css",
        "react",
        "sql",
        "git",
        "github",
        "flask",
        "swift",
        "swiftui",
        "ai",
        "machine learning",
        "data analysis",
        "excel",
        "aws",
        "azure",
        "linux",
        "networking",
        "security",
        "figma",
        "user research",
        "ui design",
        "prototyping",
        "product thinking"
    ]

    found_skills = []
    cv_text_lower = cv_text.lower()

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, cv_text_lower):
            found_skills.append(skill.title())

    return found_skills


def match_jobs(user_skills, jobs):
    matched_jobs = []

    for job in jobs:
        required_skills = job["skills"]

        matched_skills = []
        missing_skills = []

        for skill in required_skills:
            if skill in user_skills:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        match_score = int((len(matched_skills) / len(required_skills)) * 100)

        matched_jobs.append({
            "title": job["title"],
            "company": job["company"],
            "match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    matched_jobs.sort(key=lambda job: job["match_score"], reverse=True)

    return matched_jobs