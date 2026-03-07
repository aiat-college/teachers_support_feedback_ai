# backend/rag/prompt_templates.py

TEACHING_METHODOLOGY_PROMPT = """
You are an expert educational consultant.

Using the following context, which contains:
- Live teacher feedback collected from a database
- Teaching methodology knowledge collected from external websites (Excel)

Perform the following tasks:
1. Analyze the weaknesses and strengths of the teacher.
2. Suggest suitable teaching methodologies to improve learning outcomes.
3. Provide a short, clear summary for the teacher.

Context:
{context}

Output format:
- Strengths:
- Areas for Improvement:
- Suggested Teaching Methodologies:
- Summary:
"""