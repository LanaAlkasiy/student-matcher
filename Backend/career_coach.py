"""
career_coach.py

Generates the "AI Career Coach" advice + project idea shown on the
dashboard. The badge on that section already says "AI-Powered Guidance" --
this module is what makes that actually true, instead of the deterministic
f-string templates that were there before (which are NOT being thrown
away -- they're now the honest, no-API-key fallback, used automatically
when AI isn't configured).
"""

import json

from ai_client import generate_text


def generate_coaching(top_job, skills):
    """Returns {"advice": str, "project_idea": str} for the given top job
    match. Tries the LLM first; falls back to the original template logic
    on any failure so this never breaks the dashboard."""
    ai_result = _ai_coaching(top_job, skills)
    if ai_result:
        return ai_result
    return _template_coaching(top_job)


def _ai_coaching(top_job, skills):
    missing = top_job.get("missing_skills") or []

    prompt = (
        f'A student is applying for "{top_job["title"]}" at {top_job["company"]}.\n'
        f'They already have these skills: {", ".join(skills) or "none listed"}.\n'
        f'They are missing: {", ".join(missing) or "nothing -- full match"}.\n'
        f'Their match score is {top_job["match_score"]}%.\n\n'
        f"Write encouraging, specific career advice in 2-3 short sentences, "
        f"plus one concrete project idea that uses their missing skills. "
        f'Respond with ONLY JSON, no prose, no markdown fences, in this '
        f'exact shape: {{"advice": "...", "project_idea": "..."}}'
    )

    raw = generate_text(prompt)
    if not raw:
        return None

    try:
        data = json.loads(raw)
        return {"advice": data["advice"], "project_idea": data["project_idea"]}
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def _template_coaching(top_job):
    """The original rule-based logic, kept as the fallback. Still useful
    advice -- just not personalized phrasing."""
    missing = top_job.get("missing_skills") or []

    advice = (
        f"You already match {top_job['match_score']}% of the requirements "
        f"for {top_job['title']} at {top_job['company']}. Focus on closing "
        f"the remaining skill gaps to improve your chances."
    )
    project_idea = (
        f"Build a project using {missing[0]} to strengthen your profile."
        if missing else
        "Build a portfolio project showcasing your strongest skills."
    )
    return {"advice": advice, "project_idea": project_idea}
