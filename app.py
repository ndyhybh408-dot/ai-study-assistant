def study_assistant():
    print("AI Study Assistant")
    print("Welcome! How can I help you study today?")

    while True:
        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        print("AI: I'm your study assistant. Let's learn together!")


if __name__ == "__main__":
    study_assistant()
