import json


def extract_json(text: str) -> dict | None:
    """
    Robustly extract a JSON object from text that may contain
    markdown fences and trailing explanations.
    """
    if not isinstance(text, str):
        return None

    # Remove markdown fences
    cleaned = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Find the first '{'
    start = cleaned.find("{")
    if start == -1:
        return None

    # Try progressively larger substrings until JSON parses
    for end in range(len(cleaned), start, -1):
        candidate = cleaned[start:end]
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            continue

    return None