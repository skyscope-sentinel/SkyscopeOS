import os
import sqlite3
import datetime
import numpy as np
from sentence_transformers import SentenceTransformer

class SkyMemory:
    def __init__(self, db_path: str, embedder: SentenceTransformer):
        self.db_path = db_path
        self.embedder = embedder
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the SQLite database and creates the memory table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              ts TEXT,
              type TEXT,
              summary TEXT NOT NULL,
              embedding BLOB NOT NULL
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_type ON memory(type)")

    def store(self, type_: str, text: str):
        """Stores a piece of text and its corresponding vector embedding in the memory."""
        embedding = self.embedder.encode([text]).astype(np.float32).tobytes()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO memory (ts, type, summary, embedding) VALUES (?, ?, ?, ?)",
                (datetime.datetime.now().isoformat(), type_, text[:800], embedding)
            )

    def search(self, query: str, topk: int = 5) -> str:
        """Performs a semantic search for a given query and returns the most relevant memories."""
        query_vector = self.embedder.encode([query]).astype(np.float32)[0]
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT summary, embedding FROM memory").fetchall()

        if not rows:
            return "No memories found."

        scored_results = []
        for summary, embedding_blob in rows:
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            # Cosine similarity
            score = np.dot(embedding, query_vector) / (np.linalg.norm(embedding) * np.linalg.norm(query_vector))
            scored_results.append((score, summary))

        scored_results.sort(key=lambda x: x[0], reverse=True)

        top_results = scored_results[:topk]
        if not top_results:
            return "No relevant memories found."

        return "Relevant Memories:\n" + "\n".join([f"- {summary} (Score: {score:.3f})" for score, summary in top_results])
