import requests

API_KEY = "e4074e5b27msh1e8283d0b61197ap134ec8jsnfad211fef717"

def get_real_jobs(user_skills, country="us"):
    query = "software engineering internship"

    if "Data Analysis" in user_skills or "SQL" in user_skills:
        query = "data analyst internship"
    elif "Python" in user_skills or "JavaScript" in user_skills:
        query = "software engineering internship"
    elif "AI" in user_skills or "Machine Learning" in user_skills:
        query = "ai internship"

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "country": country,
        "date_posted": "week"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    jobs = []

    for item in data.get("data", [])[:10]:
        title = item.get("job_title", "Unknown Role")
        company = item.get("employer_name", "Unknown Company")
        description = item.get("job_description", "")

        skills = extract_required_skills(title + " " + description)

        jobs.append({
        "title": title,
        "company": company,
        "skills": skills,
        "url": item.get("job_apply_link", "#")
    })

    return jobs


def extract_required_skills(text):
    possible_skills = [
        "Python", "Java", "JavaScript", "HTML", "CSS", "React",
        "SQL", "Git", "GitHub", "Flask", "Swift", "SwiftUI",
        "AI", "Machine Learning", "Data Analysis", "Excel",
        "AWS", "Azure", "Linux", "Networking", "Security",
        "Figma", "User Research", "UI Design", "Prototyping"
    ]

    found = []

    text_lower = text.lower()

    for skill in possible_skills:
        if skill.lower() in text_lower:
            found.append(skill)

    if not found:
        found = ["Python", "Git", "Communication"]

    return found