import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FAISS_PATH = os.path.join(BASE_DIR, "data", "faiss_index")


def run_query(question):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = OllamaLLM(model="llama3")

    prompt = PromptTemplate.from_template(
        """
        You are an AI assistant helping teachers.
        Use the following context to answer the question.

        Context:
        {context}

        Question:
        {question}

        Answer clearly and concisely.
        """
    )

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return chain.invoke(question)


if __name__ == "__main__":
    while True:
        q = input("\nAsk a Teacher Notes question (or type exit): ")
        if q.lower() == "exit":
            break
        answer = run_query(q)
        print("\n🧠 Answer:\n", answer)
