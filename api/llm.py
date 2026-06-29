import requests

def generate_feedback(teacher, entries, context):

    prompt = f"""
You are an education expert.

Teacher: {teacher}

Entries:
{entries}

Context:
{context}

Give structured feedback.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        # SAFE extraction
        return data.get("response") or data.get("error") or str(data)

    except Exception as e:
        return f"LLM Error: {str(e)}"