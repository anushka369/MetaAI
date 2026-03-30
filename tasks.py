def grade_easy(output: str) -> float:
    target = "meeting at 5pm"

    if output.strip().lower() == target:
        return 1.0

    return 0.0


def grade_medium(output: str) -> float:
    target = "gmail.com"

    if target in output.lower():
        return 1.0

    return 0.0


def grade_hard(output: str) -> float:
    target_words = {"project", "delayed", "bug"}

    words = set(output.lower().split())

    score = len(words & target_words) / len(target_words)

    return score