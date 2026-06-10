import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQGk5W153mYDc3Ykf07IrGR304y1WWDIO3Btdo8qpYj-rKqnvFgF8wADZYqcvvS3uoRsvA066n6ZGh9/pub?output=csv"
DATA_PATH = "data"
VECTOR_PATH = "vectorstore"

def create_vectorstore():
    documents = []

    print("Fetching live data from Google Sheets...")

    # 2. Read live data directly from the Google Sheets URL
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df = df.fillna("")
        
        print("Actual columns in the sheet:", df.columns.tolist())

        # 3. Convert Google Sheet rows to documents
        for index, row in df.iterrows():
            text = f"""
### Teacher Input
Prepared: {row['What I prepared for class']}
Did Well: {row['What I did well']}
Went Well: {row['What went well']}
Needs Improvement: {row['Where to improve']}
Homework: {row['What homework did I give today']}

### Feedback
{row['Feedback']}
"""
            
            meta_tags = {
                "School": str(row.get('School/College', '')),
                "Subject": str(row.get('Subject', ''))
            }
            documents.append(Document(page_content=text,
                                       metadata={"source": f"row_{index}",
                                                 "School": meta_tags["School"],
                                                 "Subject": meta_tags["Subject"]}))
            
        print(f"Loaded {len(df)} examples from Google Sheets.")
    except Exception as e:
        print(f"Error reading from Google Sheets: {e}\nPlease check your URL and internet connection.")

    # 4. Load additional .txt files (Keeping your original logic)
    if os.path.exists(DATA_PATH):
        for file in os.listdir(DATA_PATH):
            file_path = os.path.join(DATA_PATH, file)

            if os.path.isfile(file_path) and file.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    documents.append(Document(page_content=f.read(), metadata={"source": file}))
        print("Loaded text files.")

    # 5. Create and save the Vector DB
    if len(documents) == 0:
        print("❌ ERROR: No documents were found! The database cannot be built.")
        return  # Stop the script here so it doesn't crash

    print(f"Building FAISS database with {len(documents)} documents...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(VECTOR_PATH)

    print("✅ Vector DB updated successfully with live data!")

if __name__ == "__main__":
    create_vectorstore()