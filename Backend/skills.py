"""
skills.py

Single source of truth for the skills the platform knows how to recognise,
shared by matcher.py (parsing CVs) and jobs.py (parsing job postings) so
the two sides of every match always agree on vocabulary and casing
(e.g. always "SQL", never "Sql" -- see the casing bug fixed previously).

Also now owns the actual keyword-scanning logic (find_skills_in_text), so
that logic exists in exactly one place instead of being duplicated --
slightly differently each time -- in both matcher.py and jobs.py.
"""

import re

SKILL_DISPLAY = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "node.js": "Node.js",
    "sql": "SQL",
    "git": "Git",
    "github": "GitHub",
    "flask": "Flask",
    "swift": "Swift",
    "swiftui": "SwiftUI",
    "ai": "AI",
    "machine learning": "Machine Learning",
    "data analysis": "Data Analysis",
    "excel": "Excel",
    "aws": "AWS",
    "azure": "Azure",
    "linux": "Linux",
    "networking": "Networking",
    "security": "Security",
    "figma": "Figma",
    "user research": "User Research",
    "ui design": "UI Design",
    "prototyping": "Prototyping",
    "product thinking": "Product Thinking",
    "api": "API",
    "apis": "APIs",
    "automation": "Automation",
    "workflow automation": "Workflow Automation",
    "zapier": "Zapier",
    "make": "Make",
    "n8n": "n8n",
    "power automate": "Power Automate",
    "llm": "LLM",
    "prompt engineering": "Prompt Engineering",
    "openai": "OpenAI",
    "rest api": "REST API",
}

# Common abbreviations / alternate spellings -> canonical skill name.
# Without this, a CV that says "3 years of ML" or "built with Node" never
# matches a job that says "Machine Learning" / "Node.js", even though
# they're clearly the same skill -- this was a real gap in the original
# pure-keyword extraction.
SKILL_SYNONYMS = {
    "ml": "Machine Learning",
    "js": "JavaScript",
    "ts": "TypeScript",
    "postgres": "SQL",
    "postgresql": "SQL",
    "mysql": "SQL",
    "nodejs": "Node.js",
    "node": "Node.js",
    "reactjs": "React",
    "html5": "HTML",
    "css3": "CSS",
    "genai": "AI",
    "generative ai": "AI",
}

ALL_SKILLS = list(SKILL_DISPLAY.values())


def normalize(skill: str) -> str:
    """Lowercase + strip, used as the internal key for matching."""
    return skill.strip().lower()


def to_display(skill: str) -> str:
    """Map a raw/lowercase skill string to its canonical display form."""
    key = normalize(skill)
    return SKILL_DISPLAY.get(key, skill.strip().title())


def find_skills_in_text(text: str):
    """Scan free text (a CV, a job title + description, anything) for any
    skill we recognise -- by exact name or by known synonym/abbreviation.

    This is the ONE place this logic lives. matcher.py and jobs.py both
    call this instead of each keeping their own slightly-different copy.
    Returns a sorted list of canonical (display-cased) skill names.
    """
    text_lower = text.lower()
    found = set()

    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)

    for synonym, canonical in SKILL_SYNONYMS.items():
        pattern = r"\b" + re.escape(synonym) + r"\b"
        if re.search(pattern, text_lower):
            found.add(canonical)

    return sorted(found)
