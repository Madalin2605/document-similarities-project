import re


STOPWORDS = {
    "the", "is", "and", "to", "of", "in", "a", "with",
    "can", "are", "every", "this", "that", "be",
    "for", "on", "by", "an", "it", "from"
}


def preprocess_text(text):
    # lowercase
    text = text.lower()

    # remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # tokenize
    words = text.split()

    # remove stopwords
    filtered_words = [
        word for word in words
        if word not in STOPWORDS
    ]

    return filtered_words