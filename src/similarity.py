import math
from itertools import combinations


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def compute_document_similarities(tfidf_vectors):
    similarities = []

    for doc_a, doc_b in combinations(tfidf_vectors.keys(), 2):
        score = cosine_similarity(
            tfidf_vectors[doc_a],
            tfidf_vectors[doc_b]
        )

        similarities.append((doc_a, doc_b, score))

    similarities.sort(key=lambda item: item[2], reverse=True)

    return similarities


def build_similarity_matrix(tfidf_vectors):
    """
    Builds a full similarity matrix for all documents.
    """

    document_names = list(tfidf_vectors.keys())

    matrix = {}

    for doc_a in document_names:

        matrix[doc_a] = {}

        for doc_b in document_names:

            similarity_score = cosine_similarity(
                tfidf_vectors[doc_a],
                tfidf_vectors[doc_b]
            )

            matrix[doc_a][doc_b] = similarity_score

    return matrix


def get_top_similar_documents(similarities, top_n=3):
    """
    Returns the top N most similar document pairs.
    """

    return similarities[:top_n]