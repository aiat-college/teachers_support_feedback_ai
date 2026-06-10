def generate(text_context, video_context):
    feedback = " ".join(text_context[:3])

    return {
        "feedback": feedback,
        "videos": video_context
    }