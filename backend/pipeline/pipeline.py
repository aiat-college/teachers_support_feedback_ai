from ingest.ingest_db import ingest_teachernotes_db
from ingest.ingest_excel import ingest_methodology_excel
from core.vectordb import create_vectorstore
from rag.retriever import retrieve
from core.generator import generate
from utils.save_outputs import save_teacher_output

def run_pipeline():
    teacher_feedback = ingest_teachernotes_db()
    methodology_docs = ingest_methodology_excel("data/excel/methodology.xlsx")

    # Combine all docs once
    all_docs = []
    for feedback_docs in teacher_feedback.values():
        all_docs += feedback_docs
    all_docs += methodology_docs

    if not all_docs:
        print("No documents found. Aborting pipeline.")
        return

    # Create vectorstore once
    vectorstore = create_vectorstore(all_docs)

    for teacher in teacher_feedback.keys():
        query = "Suggest teaching methodologies based on the teacher's feedback"
        context = retrieve(vectorstore, query)
        output = generate(context)
        save_teacher_output(teacher, output)
