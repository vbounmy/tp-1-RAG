from vector_db import VectorDB
from vector_db import VectorDB

if __name__ == "__main__":
    db = VectorDB(collection_name="chroma_db")
    print(f"Base construite : {db.collection.count()} chunks indexés.")