
from scripts.chatbot.generateResponse import generate_answer_with_images
from scripts.chatbot.retrieveData import retrieve_relevant_data

if __name__ == "__main__":
    # Example Usage
    question = input("Ask me a question: ")
    retrieval_results = retrieve_relevant_data(question)
    answer = generate_answer_with_images(question, retrieval_results)

    print(answer)  # Displays the OpenAI-generated response