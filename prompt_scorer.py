import re


def analyze_prompt(prompt):

    score = 0

    improvements = []

    prompt_lower = prompt.lower()

    words = prompt.split()

    word_count = len(words)

    if word_count >= 20:
        score += 15
    else:
        improvements.append(
            "Provide more details to make the prompt more informative."
        )

    objective_keywords = [
        "create",
        "write",
        "generate",
        "build",
        "design",
        "develop",
        "explain",
        "summarize",
        "analyze"
    ]

    if any(word in prompt_lower for word in objective_keywords):
        score += 15
    else:
        improvements.append(
            "Clearly describe the objective of your prompt."
        )

    context_keywords = [
        "for",
        "about",
        "using",
        "with",
        "based on",
        "related to"
    ]

    if any(keyword in prompt_lower for keyword in context_keywords):
        score += 15
    else:
        improvements.append(
            "Add context so the AI understands your request better."
        )

    role_keywords = [
        "you are",
        "act as",
        "expert",
        "assistant"
    ]

    if any(keyword in prompt_lower for keyword in role_keywords):
        score += 15
    else:
        improvements.append(
            "Specify the role you want the AI to assume."
        )

    constraint_keywords = [
        "only",
        "must",
        "should",
        "without",
        "avoid",
        "include"
    ]

    if any(keyword in prompt_lower for keyword in constraint_keywords):
        score += 10
    else:
        improvements.append(
            "Add constraints or requirements to guide the AI."
        )

    format_keywords = [
        "table",
        "json",
        "markdown",
        "bullet",
        "list",
        "code",
        "format"
    ]

    if any(keyword in prompt_lower for keyword in format_keywords):
        score += 10
    else:
        improvements.append(
            "Specify the desired output format."
        )

    if "\n" in prompt or ":" in prompt:
        score += 10
    else:
        improvements.append(
            "Structure the prompt using sections or line breaks."
        )


    if word_count >= 10:
        score += 10
    else:
        improvements.append(
            "Make the prompt more specific."
        )

    score = min(score, 100)

    if score >= 90:
        level = "Excellent"

    elif score >= 75:
        level = "Very Good"

    elif score >= 60:
        level = "Good"

    elif score >= 40:
        level = "Needs Improvement"

    else:
        level = "Poor"

    return {

        "score": score,

        "level": level,

        "improvements": improvements

    }