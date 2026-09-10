from app.pipeline import user_query

def main():
    print("\n====================== || RAG Chatbot || ======================")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("[-] You: ").strip()

        # Exit the chat
        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Ignore empty input
        if not query:
            continue

        try:
            # Run the RAG pipeline
            answer = user_query(query)
            print(f"[+] Assistant: {answer}\n")

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()