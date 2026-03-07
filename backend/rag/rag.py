from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from backend.db.teacher_input_repo import get_latest_teacher_input



# ----------------------------
# Load Vector Store
# ----------------------------
def load_vectorstore():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

    return db


# ----------------------------
# Retrieve Context
# ----------------------------
def retrieve_context(query, vectordb, k=4):
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)

    if not docs:
        return ""

    return "\n\n".join(doc.page_content for doc in docs)



# ----------------------------
# Generate Answer
# ----------------------------
def generate_answer(query, context):
    llm = OllamaLLM(model="llama3.2:1b")

    prompt = f"""
Answer ONLY using the context below.
If not available say:
"No relevant data available in provided materials."

Context:
{context}

Question:
{query}
"""
    return llm.invoke(prompt)


# ----------------------------
# MAIN RAG FUNCTION
# ----------------------------
def generate_feedback_from_latest_teacher_input():
    teacher_input = get_latest_teacher_input()

    query = (
        f"{teacher_input['question']} "
        f"(Subject: {teacher_input['subject']}, "
        f"Class: {teacher_input['class']}, "
        f"Category: {teacher_input['category']})"
    )

    vectordb = load_vectorstore()
    context = retrieve_context(query, vectordb)
    answer = generate_answer(query, context)

    return {
        "input_id": teacher_input["id"],
        "question": teacher_input["question"],
        "answer": answer
    }
if __name__ == "__main__":
    result = generate_feedback_from_latest_teacher_input()
    print(result)
