"""
ai_client.py

One tiny wrapper around an LLM call so the rest of the app never has to
know which provider is configured, and so every AI feature shares the
exact same fail-safe behavior: if there's no key, or the call errors out,
this returns None and the *caller* decides what to do (almost always:
fall back to the deterministic template that already existed).

This mirrors the pattern already used in jobs.get_real_jobs() -- try the
smart path, fall back to something simpler and reliable on any failure.

Swap the body of generate_text() for the OpenAI or Gemini SDK if you'd
rather use those -- nothing else in the codebase needs to change, since
every caller only ever sees "plain text in, plain text out (or None)".
"""

import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"


def generate_text(prompt, system=None, max_tokens=300):
    """Returns the model's reply as a string, or None on any failure.

    Deliberately swallows all errors (missing key, network issue, bad
    response, rate limit) -- callers must already have a non-AI fallback,
    so a None here should never crash a request.
    """
    if not ANTHROPIC_API_KEY:
        return None

    try:
        import anthropic  # imported lazily so the package is optional
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system or "",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as error:  # noqa: BLE001 -- intentionally broad, see docstring
        print(f"[ai_client] LLM call failed: {error}")
        return None
