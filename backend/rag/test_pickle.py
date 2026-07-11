import pickle

with open("vectorstore/books_faiss/index.pkl", "rb") as f:
    data = pickle.load(f)

print("TYPE:", type(data))

if isinstance(data, tuple):
    print("TUPLE LENGTH:", len(data))

    for i, item in enumerate(data):
        print(f"ITEM {i}: {type(item)}")