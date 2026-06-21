"""
jobs.py

Fetches live job/internship postings from the JSearch API (RapidAPI).
This is the ONLY module that should do this -- job_api.py used to contain
a second, older, duplicate copy of this same logic (no error handling, no
timeout, no shared skill taxonomy, and a hardcoded RapidAPI key). app.py
already only imports from here, so job_api.py is dead code and should be
deleted from the repo to avoid two versions of the truth drifting apart.

Supports a few different opportunity types via `opportunity_type`, since
"internship" was the only thing ever searched for before. Hackathons are
NOT available through this API (JSearch indexes job postings, not events)
-- that needs a separate source (e.g. Devpost's public API) plugged in
behind the same `get_real_jobs`-shaped interface later. Stubbed below so
the seam is visible.
"""

import os

import requests
from dotenv import load_dotenv

from skills import ALL_SKILLS

load_dotenv()

API_KEY = os.environ.get("RAPIDAPI_KEY")
REQUEST_TIMEOUT_SECONDS = 8

# One query template per opportunity type. "{}" is filled with a skill-based
# focus area (e.g. "software engineering", "data analyst").
QUERY_TEMPLATES = {
    "internship": "{} internship",
    "graduate": "{} graduate program",
    "training": "{} traineeship",
}


def get_real_jobs(user_skills, country="us", opportunity_type="internship"):
    """Fetch live postings from JSearch. Returns [] on ANY failure --
    missing key, network error, bad response, rate limit, unknown
    opportunity_type -- so callers can fall back to the local curated list
    rather than crashing the request."""
    if not API_KEY:
        print("[jobs] RAPIDAPI_KEY is not set -- skipping live job search.")
        return []

    template = QUERY_TEMPLATES.get(opportunity_type, QUERY_TEMPLATES["internship"])
    focus = _focus_area(user_skills)
    query = template.format(focus)

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
        print(f"[jobs] Request to JSearch failed: {error}")
        return []
    except ValueError as error:
        print(f"[jobs] Could not parse JSearch response as JSON: {error}")
        return []

    jobs = []
    for item in data.get("data", [])[:10]:
        title = item.get("job_title", "Unknown Role")
        company = item.get("employer_name", "Unknown Company")
        description = item.get("job_description", "")

        jobs.append({
            "title": title,
            "company": company,
            "skills": extract_required_skills(title + " " + description),
            "url": item.get("job_apply_link", "#"),
            # These two were previously hardcoded as "Internship"/"Remote"
            # in the frontend regardless of the real posting -- now sourced
            # from the actual API response.
            "employment_type": _humanize_employment_type(item.get("job_employment_type")),
            "location": _humanize_location(item),
        })

    return jobs


def _focus_area(user_skills):
    if "Data Analysis" in user_skills or "SQL" in user_skills:
        return "data analyst"
    if "AI" in user_skills or "Machine Learning" in user_skills:
        return "ai"
    return "software engineering"


def _humanize_employment_type(raw):
    mapping = {
        "FULLTIME": "Full-time",
        "PARTTIME": "Part-time",
        "INTERN": "Internship",
        "CONTRACTOR": "Contract",
    }
    return mapping.get((raw or "").upper(), "Internship")


def _humanize_location(item):
    if item.get("job_is_remote"):
        return "Remote"
    city = item.get("job_city")
    country = item.get("job_country")
    if city and country:
        return f"{city}, {country}"
    return city or country or "Location N/A"


def extract_required_skills(text):
    """Keyword-match the known skill taxonomy against a job title +
    description. This is "tier 1" extraction -- fast, free, and exact, but
    only catches skills literally named in the text. See the project
    write-up for the planned "tier 2" semantic fallback using an LLM for
    postings phrased in ways that don't literally mention a skill name."""
    text_lower = text.lower()
    found = [skill for skill in ALL_SKILLS if skill.lower() in text_lower]

    if not found:
        found = ["Python", "Git", "Communication"]

    return found


def get_hackathons():
    """Not implemented: JSearch has no hackathon data. Wire up a real
    source (e.g. Devpost's public API) here later, returning the same
    shape as get_real_jobs() so app.py doesn't need to change."""
    return []
