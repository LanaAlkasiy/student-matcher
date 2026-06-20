# skills.py
#
# Single source of truth for the skills the platform knows how to recognise.
# Both matcher.py (parsing the uploaded CV) and job_api.py (parsing live job
# postings) import this so the two sides of the match always speak the same
# vocabulary and use the same casing (e.g. "SQL", not "Sql").

SKILL_DISPLAY = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "react": "React",
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
}

# Ordered list of the canonical (display-cased) skill names, derived from the
# map above so there is only ever one place to add a new skill.
ALL_SKILLS = list(SKILL_DISPLAY.values())


def normalize(skill: str) -> str:
    """Lowercase + strip, used as the internal key for matching."""
    return skill.strip().lower()


def to_display(skill: str) -> str:
    """Map a raw/lowercase skill string to its canonical display form."""
    key = normalize(skill)
    return SKILL_DISPLAY.get(key, skill.strip().title())
