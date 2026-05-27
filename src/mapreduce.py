from collections import Counter
from src.preprocessing import preprocess_text


def map_word_count(document_data):
    """
    MAP FUNCTION

    Processes a single document:
    - preprocesses text
    - counts word frequencies

    Returns:
    (document_name, word_frequencies)
    """

    document_name, content = document_data

    words = preprocess_text(content)
    word_counts = Counter(words)

    return document_name, word_counts


def reduce_document_frequency(map_results):
    """
    REDUCE FUNCTION

    Computes document frequency for each word:
    in how many documents each word appears.
    """

    document_frequency = Counter()

    for document_name, word_counts in map_results:
        unique_words = set(word_counts.keys())

        for word in unique_words:
            document_frequency[word] += 1

    return document_frequency


def build_global_vocabulary(map_results):
    """
    Builds the global vocabulary from all documents.
    """

    vocabulary = set()

    for document_name, word_counts in map_results:
        vocabulary.update(word_counts.keys())

    return sorted(vocabulary)