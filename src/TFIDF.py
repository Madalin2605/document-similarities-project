import math


def compute_tfidf_vectors(map_results, document_frequency, vocabulary):
    """
    Computes TF-IDF vectors for all documents.
    """

    total_documents = len(map_results)
    tfidf_vectors = {}

    for document_name, word_counts in map_results:
        total_words = sum(word_counts.values())
        vector = []

        for word in vocabulary:
            term_frequency = word_counts.get(word, 0) / total_words

            inverse_document_frequency = math.log(
                (1 + total_documents) / (1 + document_frequency.get(word, 0))
            ) + 1

            tfidf_score = term_frequency * inverse_document_frequency
            vector.append(tfidf_score)

        tfidf_vectors[document_name] = vector

    return tfidf_vectors