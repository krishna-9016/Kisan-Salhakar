import faiss
import pickle

faiss_index = faiss.read_index("vector_store/faiss_index.bin")
with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print("FAISS ntotal:", faiss_index.ntotal)
print("Chunks length:", len(chunks))
