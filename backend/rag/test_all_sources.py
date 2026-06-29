from backend.rag.query import retrieve_context

context = retrieve_context(
    "Students struggled with word problems and place value."
)

print(context)