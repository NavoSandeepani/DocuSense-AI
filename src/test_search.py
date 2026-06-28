from semantic_search import build_index, search

text = """
Python is used in Machine Learning.
University of Jaffna offers Computer Engineering.
FAISS is used for semantic search.
"""

index, chunks = build_index(text)

results = search(
    "Where can I study Computer Engineering?",
    index,
    chunks
)

print(results)