# Round 1B Approach Explanation

We used a semantic similarity-based approach to identify and rank relevant document sections. The model used is `all-MiniLM-L6-v2` from SentenceTransformers (~80MB), which encodes both the task query (persona + job-to-be-done) and section content into embeddings. We calculate cosine similarity between query and section embeddings, then rank them accordingly.

Text is extracted using PyMuPDF for its accuracy in preserving layout. We filter by paragraph length and split across multiple documents. The final result includes top 10 most relevant sections across all PDFs, complete with `importance_rank`, `refined_text`, and page metadata.

This approach is generic, lightweight (within 1GB model size), runs fully offline, and processes input in less than 60 seconds for a small set of PDFs.