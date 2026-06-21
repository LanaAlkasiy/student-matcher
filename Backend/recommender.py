"""
recommender.py

Turns a list of missing skills into course recommendations.

Why this exists: the old logic lived entirely in index.html as a 8-entry
hardcoded `courseMap`, computed client-side. Any skill not in that map fell
back to a generic, obviously-fake placeholder ("X Fundamentals" / "Online" /
"Self-paced"), which is exactly the "feels fake and rule-based" problem.

This module fixes that with three tiers, each one only used when the
previous one has nothing to offer:

  1. CURATED_CATALOG  -- hand-picked, accurate, instant, free. Lives in
     curated_courses.json so it's easy to keep growing without touching
     code.
  2. AI-generated suggestion -- only triggered for a skill with no catalog
     entry. Cached (functools.lru_cache) so the same skill is never sent
     to the LLM twice in a process's lifetime -- this is the same skill
     gap across thousands of students, there's no reason to pay for the
     same answer repeatedly.
  3. Generic "go search for it" fallback -- only reached if there's no
     catalog entry AND no AI key configured (or the call failed). Still
     functional, just not pretending to be smarter than it is.

Each returned recommendation includes "source" so the frontend can (if it
wants to) visually distinguish curated vs AI-suggested vs generic --
honesty about confidence level is part of *not* feeling fake.
"""

import json
from functools import lru_cache
from pathlib import Path

from ai_client import generate_text

CATALOG_PATH = Path(__file__).parent / "curated_courses.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    CURATED_CATALOG = json.load(f)


def recommend_courses(missing_skills, limit=3):
    """Return up to `limit` course recommendations, one per missing skill,
    preferring curated catalog entries and falling back to AI / generic
    suggestions only when needed."""
    recommendations = []

    for skill in missing_skills[:limit]:
        course = CURATED_CATALOG.get(skill)
        if course:
            recommendations.append({**course, "skill": skill, "source": "curated"})
            continue

        ai_course = _ai_course_suggestion(skill)
        if ai_course:
            recommendations.append({**ai_course, "skill": skill, "source": "ai"})
            continue

        recommendations.append({
            "name": f'Search for "{skill}" courses',
            "provider": "Self-directed",
            "duration": "Varies",
            "color": "#6b7280",
            "skill": skill,
            "source": "fallback",
        })

    return recommendations


@lru_cache(maxsize=256)
def _ai_course_suggestion(skill):
    """Ask the LLM for ONE realistic course suggestion for `skill`.

    Cached per skill (not per user) -- "what should someone learning SQL
    take" has the same good answer regardless of who's asking, so caching
    here is free accuracy, not a corner cut.

    Returns None if no AI key is configured or the response can't be
    parsed -- caller already has the generic fallback for that case.
    """
    prompt = (
        f'Suggest exactly one real, well-known online course or learning '
        f'resource for someone who needs to learn "{skill}" for an '
        f"internship application.\n\n"
        f"Respond with ONLY a JSON object, no prose, no markdown fences, "
        f'in this exact shape: {{"name": "<course name>", '
        f'"provider": "<platform, e.g. Coursera>", "duration": "<e.g. 4 hours>"}}'
    )

    raw = generate_text(prompt)
    if not raw:
        return None

    try:
        data = json.loads(raw)
        return {
            "name": data["name"],
            "provider": data["provider"],
            "duration": data.get("duration", "Self-paced"),
            # Distinct color so an AI-sourced suggestion is visually
            # flaggable in the UI later if you want a "Suggested by AI" tag.
            "color": "#7c3aed",
        }
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
