import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean_text, chunk_text

def build_vector_store():
    # Load and chunk all documents
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_index": i,
                "text": chunk
            })

    print(f"Embedding {len(all_chunks)} chunks...")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it already exists
    try:
        client.delete_collection("rutgers_dining")
    except:
        pass
    
    collection = client.create_collection("rutgers_dining")

    # Embed and store chunks
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in all_chunks],
        ids=[f"{c['source']}_{c['chunk_index']}" for c in all_chunks]
    )

    print("Done! Vector store built.")
    return collection, model

def retrieve(query, model, collection, k=5):
    query_embedding = model.encode([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )
    return results

if __name__ == "__main__":
    collection, model = build_vector_store()
    
    # Test retrieval with 3 evaluation questions
    test_queries = [
        "Which dining hall is the best at Rutgers?",
        "What meal plan should a freshman get?",
        "What is Henry's Diner like?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retrieve(query, model, collection)
        for doc, meta, distance in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            print(f"  [{distance:.3f}] ({meta['source']}) {doc[:100]}")