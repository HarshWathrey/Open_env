def grade_easy(action):
    score = 0.0
    if action.get("priority") == "medium":
        score += 0.5
    if action.get("action_type") == "respond":
        score += 0.5
    return round(score, 2)


def grade_medium(trace):
    score = 0.0

    if any(a.get("priority") == "high" for a in trace):
        score += 0.3

    if any(a.get("action_type") == "escalate" for a in trace):
        score += 0.4

    if any("refund" in (a.get("message") or "").lower() for a in trace):
        score += 0.3

    return round(score, 2)


def grade_hard(trace):
    score = 0.0

    if any(a.get("action_type") == "request_info" for a in trace):
        score += 0.2

    if any(a.get("priority") in ["high","urgent"] for a in trace):
        score += 0.3

    if any(a.get("action_type") == "respond" for a in trace):
        score += 0.5

    return round(score, 2)