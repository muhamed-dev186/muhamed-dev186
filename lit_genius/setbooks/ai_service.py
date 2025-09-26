import openai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- OpenAI/OpenRouter Client ---
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# --- Embedding Model ---
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- In-memory Vector Store (FAISS) ---
# For simplicity, we'll use a global in-memory index.
# In a real application, this should be managed more robustly (e.g., persisted to disk, managed per-book).
dimension = embedding_model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)
chapter_id_map = [] # Maps index position to chapter ID

def add_chapter_to_index(chapter_id, content):
    """Generates embedding for chapter content and adds it to the FAISS index."""
    embedding = embedding_model.encode([content])
    index.add(np.array(embedding, dtype=np.float32))
    chapter_id_map.append(chapter_id)
    print(f"Added chapter {chapter_id} to index. Index size: {index.ntotal}")

def search_index(query, k=5):
    """Searches the index for the most relevant chapters to the query."""
    if index.ntotal == 0:
        return []
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), k)

    # Return the chapter IDs of the top k results
    return [chapter_id_map[i] for i in indices[0]]

# --- LLM Functions ---

def summarize_text(text):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes texts."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"},
        ],
    )
    return response.choices[0].message.content

def answer_question(question, context):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. Be concise and directly answer the question."},
            {"role": "user", "content": f"Based on the following context, please answer the question.\n\nContext:\n{' '.join(context)}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content
