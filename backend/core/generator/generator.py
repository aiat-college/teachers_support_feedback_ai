def generate(text_context, website_context):
    """
    Generates teaching suggestions strictly from:
    - Teacher feedback (DB)
    - Teaching methodology websites (Excel / scraped text)
    No hallucination
    """

    # --- 1. Feedback summary ---
    feedback_summary = " ".join(text_context[:3])

    # --- 2. Methodology suggestions from websites ---
    methodology_suggestions = []

    for site in website_context:
        content = site.lower()

        if "active learning" in content:
            methodology_suggestions.append(
                "Adopt Active Learning techniques as suggested in teaching methodology websites."
            )

        if "flipped classroom" in content:
            methodology_suggestions.append(
                "Use the Flipped Classroom approach as recommended by external teaching websites."
            )

        if "project based learning" in content:
            methodology_suggestions.append(
                "Implement Project-Based Learning methods based on website guidance."
            )

        if "assessment rubric" in content:
            methodology_suggestions.append(
                "Use structured assessment rubrics as described in methodology resources."
            )

    if not methodology_suggestions:
        methodology_suggestions.append(
            "No specific methodology recommendations were retrieved from external websites."
        )

    return {
        "feedback_summary": feedback_summary,
        "methodology_suggestions": list(set(methodology_suggestions))
    }
