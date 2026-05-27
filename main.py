from pathlib import Path
from multiprocessing import Pool, cpu_count
import time

from src.preprocessing import preprocess_text
from src.mapreduce import (
    map_word_count,
    reduce_document_frequency,
    build_global_vocabulary,
)
from src.TFIDF import compute_tfidf_vectors
from src.similarity import (
    compute_document_similarities,
    build_similarity_matrix,
    get_top_similar_documents,
)
from src.exporter import (
    export_similarities_to_csv,
    export_similarity_matrix_to_csv,
)


# DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"
DOCUMENTS_DIR = Path(__file__).resolve().parent / "benchmark_documents"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def load_documents():
    documents = {}

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            documents[file_path.name] = file.read()

    return documents


def prepare_documents(documents):
    prepared_data = []

    for document_name, content in documents.items():
        prepared_data.append(
            (document_name, content)
        )

    return prepared_data


def sequential_map_processing(prepared_data):
    results = []

    for document_data in prepared_data:
        result = map_word_count(document_data)
        results.append(result)

    return results


def main():

    documents = load_documents()
    prepared_data = prepare_documents(documents)

    print(f"\nUsing {cpu_count()} CPU cores\n")

    # SEQUENTIAL PROCESSING
    sequential_start = time.perf_counter()
    sequential_results = sequential_map_processing(prepared_data)
    sequential_end = time.perf_counter()
    sequential_time = sequential_end - sequential_start

    # PARALLEL PROCESSING
    parallel_start = time.perf_counter()
    with Pool() as pool:

        results = pool.map(
            map_word_count,
            prepared_data
        )

    parallel_end = time.perf_counter()
    parallel_time = parallel_end - parallel_start

    # PERFORMANCE RESULTS
    print("PERFORMANCE BENCHMARK:\n")
    print(f"Sequential Processing Time: {sequential_time:.6f} seconds")
    print(f"Parallel Processing Time:   {parallel_time:.6f} seconds")

    if parallel_time > 0:
        speedup = sequential_time / parallel_time
        print(f"Speedup: {speedup:.2f}x\n")
    
    # REDUCE STEP
    document_frequency = reduce_document_frequency(results)
    global_vocabulary = build_global_vocabulary(results)

    print("GLOBAL VOCABULARY:\n")
    print(global_vocabulary)

    print("\nDOCUMENT FREQUENCY:\n")
    for word, frequency in document_frequency.items():
        print(f"{word}: {frequency}")

    # TF-IDF STEP
    tfidf_vectors = compute_tfidf_vectors(
        results,
        document_frequency,
        global_vocabulary
    )

    # SIMILARITY STEP
    similarities = compute_document_similarities(tfidf_vectors)

    # SIMILARITY MATRIX
    similarity_matrix = build_similarity_matrix(tfidf_vectors)

    # TOP SIMILAR DOCUMENTS
    top_similarities = get_top_similar_documents(
        similarities,
        top_n=3
    )
    
    print("\nTOP 3 MOST SIMILAR DOCUMENT PAIRS:\n")
    for index, (doc_a, doc_b, score) in enumerate(top_similarities, start=1):

        print(
            f"{index}. "
            f"{doc_a} <-> {doc_b} "
            f"=> Similarity Score: {score:.4f}"
        )
    
    # EXPORT RESULTS
    OUTPUT_DIR.mkdir(exist_ok=True)

    export_similarities_to_csv(
        similarities,
        OUTPUT_DIR / "document_similarities.csv"
    )

    export_similarity_matrix_to_csv(
        similarity_matrix,
        OUTPUT_DIR / "similarity_matrix.csv"
    )

    print("\nResults exported successfully:")
    print("- output/document_similarities.csv")
    print("- output/similarity_matrix.csv")


if __name__ == "__main__":
    main()