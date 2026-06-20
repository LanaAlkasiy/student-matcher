import os

import requests
from dotenv import load_dotenv

from skills import ALL_SKILLS

# Loads variables from a local .env file (gitignored) into the environment.
# In production (e.g. a host like Render/Railway), set RAPIDAPI_KEY as a
# real environment variable instead and this call is a harmless no-op.
load_dotenv()

API_KEY = os.environ.get("RAPIDAPI_KEY")
REQUEST_TIMEOUT_SECONDS = 8


def get_real_jobs(user_skills, country="us"):
    """Fetch live internship/job postings from the JSearch API.

    Returns [] (instead of raising) on any failure -- missing key, network
    error, bad response, rate limit, etc. -- so callers can fall back to the
    local curated job list rather than crashing the request.
    """
    if not API_KEY:
        print("[job_api] RAPIDAPI_KEY is not set -- skipping live job search.")
        return []

    query = "software engineering internship"

    if "Data Analysis" in user_skills or "SQL" in user_skills:
        query = "data analyst internship"
    elif "AI" in user_skills or "Machine Learning" in user_skills:
        query = "ai internship"
    elif "Python" in user_skills or "JavaScript" in user_skills:
        query = "software engineering internship"

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "country": country,
        "date_posted": "week",
    }

    try:
        response = requests.get(
            url, headers=headers, params=params, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as error:
        print(f"[job_api] Request to JSearch failed: {error}")
        return []
    except ValueError as error:
        print(f"[job_api] Could not parse JSearch response as JSON: {error}")
        return []

    jobs = []

    for item in data.get("data", [])[:10]:
        title = item.get("job_title", "Unknown Role")
        company = item.get("employer_name", "Unknown Company")
        description = item.get("job_description", "")

        required_skills = extract_required_skills(title + " " + description)

        jobs.append({
            "title": title,
            "company": company,
            "skills": required_skills,
            "url": item.get("job_apply_link", "#"),
        })

    return jobs


def extract_required_skills(text):
    """Scan a job title/description for any skill we recognise.

    Uses the same canonical skill list as matcher.py (skills.ALL_SKILLS) so
    a job's required skills and a CV's extracted skills are always written
    the same way (e.g. always "SQL", never "Sql").
    """
    text_lower = text.lower()

    found = [skill for skill in ALL_SKILLS if skill.lower() in text_lower]

    if not found:
        found = ["Python", "Git", "Communication"]

    return found
