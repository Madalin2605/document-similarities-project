import csv
from pathlib import Path


def export_similarities_to_csv(similarities, output_path):
    output_path = Path(output_path)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["document_a", "document_b", "similarity_score"])

        for doc_a, doc_b, score in similarities:
            writer.writerow([doc_a, doc_b, round(score, 4)])


def export_similarity_matrix_to_csv(similarity_matrix, output_path):
    output_path = Path(output_path)

    document_names = list(similarity_matrix.keys())

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["document"] + document_names)

        for row_name in document_names:
            row = [row_name]

            for col_name in document_names:
                row.append(round(similarity_matrix[row_name][col_name], 4))

            writer.writerow(row)