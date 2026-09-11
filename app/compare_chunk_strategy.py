from app.ingest import (chunk_text_fixed_size, chunk_recursive, load_document)
import os
from app.config import DATA_DIR


def compare_chunking(filename: str, text: str):
    fixed = chunk_text_fixed_size(text)
    recursive = chunk_recursive(text)

    print("Fixed size:")
    print(f"           Total: [{len(fixed)}]")
    print("           " + "=" * 50)
    for i, _ in enumerate(fixed, start=1):
        print(f"           Chunk {i}: {filename}")
    print()

    print("Recursive:")
    print(f"           Total: [{len(recursive)}]")
    print("           " + "=" * 50)
    for i, _ in enumerate(recursive, start=1):
        print(f"           Chunk {i}: {filename}")
    print()


if __name__ == '__main__':
    while True:
        try:
            count_file = int(input("Enter number of files to load: ").strip())
            if count_file <= 0:
                print("Error: Number of files must be greater than 0.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    while True:
        data_dir = input(f"Enter document folder [default: {DATA_DIR}]: ").strip()

        if not data_dir:
            data_dir = DATA_DIR

        if not os.path.exists(data_dir):
            print(f"Error: Folder does not exist: {data_dir}")
            continue

        if not os.path.isdir(data_dir):
            print(f"Error: This path is not a folder: {data_dir}")
            continue

        break

    documents = load_document(count_file, data_dir)

    if not documents:
        raise FileNotFoundError(f"No file .txt was found in directory {data_dir}/")

    for filename, full_text in documents:
        print(f"\n{'=' * 80}")
        print(f"|| File: {filename}")
        print(f"{'=' * 80}\n")
        compare_chunking(filename, full_text)