# backend/ingest/ingest_excel.py
import pandas as pd

def ingest_methodology_excel(path):
    df = pd.read_excel(path)
    docs = []

    for _, row in df.iterrows():
        docs.append(
            f"Teaching Method: {row['Method']} "
            f"Benefit: {row['Improves']} "
            f"Details: {row['Description']}"
        )

    return docs
