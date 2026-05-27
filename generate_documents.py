from pathlib import Path
import random


OUTPUT_DIR = Path(__file__).resolve().parent / "benchmark_documents"

DOCUMENTS_PER_CATEGORY = 200

CATEGORIES = {
    "ai": [
        "artificial intelligence", "machine learning", "data analysis",
        "neural networks", "prediction models", "automation",
        "large datasets", "pattern recognition", "deep learning",
        "natural language processing"
    ],
    "cooking": [
        "cooking recipes", "fresh ingredients", "tomato sauce",
        "pasta preparation", "kitchen tools", "boiling water",
        "healthy meals", "food taste", "baking bread",
        "meal planning"
    ],
    "sports": [
        "football training", "team strategy", "player performance",
        "strength exercises", "speed improvement", "match preparation",
        "discipline", "teamwork", "competition", "fitness"
    ],
    "finance": [
        "financial markets", "investment strategy", "stock prices",
        "risk management", "portfolio analysis", "economic growth",
        "banking services", "interest rates", "profit margins",
        "business decisions"
    ],
    "health": [
        "medical research", "healthy lifestyle", "physical exercise",
        "mental health", "nutrition plans", "patient care",
        "disease prevention", "public health", "doctor consultation",
        "wellness habits"
    ],
}


def generate_document(category_name, keywords, index):
    selected_keywords = random.choices(keywords, k=3000)

    paragraphs = []

    for paragraph_index in range(30):
        start = paragraph_index * 100
        end = start + 100

        paragraph_keywords = selected_keywords[start:end]

        paragraph = (
            f"This document is about {category_name}. "
            f"It discusses {' '.join(paragraph_keywords)}. "
            f"The text belongs to the {category_name} category."
        )

        paragraphs.append(paragraph)

    return "\n".join(paragraphs)


def main():
    random.seed(42)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for category_name, keywords in CATEGORIES.items():
        for index in range(1, DOCUMENTS_PER_CATEGORY + 1):
            file_name = f"{category_name}_{index}.txt"
            file_path = OUTPUT_DIR / file_name

            content = generate_document(category_name, keywords, index)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

    total_documents = DOCUMENTS_PER_CATEGORY * len(CATEGORIES)

    print(f"Generated {total_documents} benchmark documents in:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()