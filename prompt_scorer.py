import re


OBJECTIVE_KEYWORDS = {
    "write", "create", "generate", "build", "design",
    "develop", "explain", "summarize", "analyze",
    "optimize", "convert", "translate", "draft"
}


ROLE_KEYWORDS = {
    "you are", "act as", "expert", "assistant",
    "developer", "engineer", "writer", "analyst"
}


FORMAT_KEYWORDS = {
    "markdown", "json", "table", "list",
    "bullet", "code", "format"
}


CONSTRAINT_KEYWORDS = {
    "must", "should", "only", "without",
    "avoid", "include", "ensure", "don't"
}


def contains_keywords(text, keywords):

    text = text.lower()

    return any(keyword in text for keyword in keywords)


def analyze_prompt(prompt):

    score = 0

    improvements = []

    prompt_lower = prompt.lower()

    word_count = len(prompt.split())


    if word_count >= 40:

        score += 15

    elif word_count >= 20:

        score += 10

    elif word_count >= 10:

        score += 6

    else:

        improvements.append(
            "Added more descriptive details."
        )

    if contains_keywords(prompt_lower, OBJECTIVE_KEYWORDS):

        score += 15

    else:

        improvements.append(
            "Clarified the objective."
        )


    if contains_keywords(prompt_lower, ROLE_KEYWORDS):

        score += 15

    else:

        improvements.append(
            "Added a professional AI role."
        )


    if any(word in prompt_lower for word in [
        "for",
        "using",
        "with",
        "about",
        "based on"
    ]):

        score += 12

    else:

        improvements.append(
            "Added relevant context."
        )

    if contains_keywords(prompt_lower, CONSTRAINT_KEYWORDS):

        score += 12

    else:

        improvements.append(
            "Added clear requirements and constraints."
        )


    if contains_keywords(prompt_lower, FORMAT_KEYWORDS):

        score += 10

    else:

        improvements.append(
            "Defined the expected output format."
        )


    structure_score = 0

    if "\n" in prompt:

        structure_score += 4

    if ":" in prompt:

        structure_score += 4

    if "-" in prompt or "*" in prompt:

        structure_score += 2

    score += structure_score

    if structure_score < 8:

        improvements.append(
            "Improved prompt structure."
        )

    unique_words = len(set(re.findall(r"\w+", prompt_lower)))

    if unique_words >= 50:

        score += 11

    elif unique_words >= 25:

        score += 8

    elif unique_words >= 10:

        score += 5

    else:

        improvements.append(
            "Made the prompt more specific."
        )


    score = min(score, 98)


    if score >= 92:

        level = "Outstanding"

    elif score >= 82:

        level = "Excellent"

    elif score >= 70:

        level = "Strong"

    elif score >= 55:

        level = "Good"

    else:

        level = "Needs Improvement"


    return {

        "score": score,

        "level": level,

        "improvements": improvements

    }