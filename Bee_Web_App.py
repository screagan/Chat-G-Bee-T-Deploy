import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from scripts.chatbot.generateResponse import generate_answer_with_images
from scripts.chatbot.retrieveData import retrieve_relevant_data

st.title("ChatG-🐝: Your Bee Knowledge Assistant")

def generate_response(input_text):
    retrieval_results = retrieve_relevant_data(input_text)
    images, answer = generate_answer_with_images(input_text, retrieval_results)
    return images, answer

with st.form("my_form"):
    question = st.text_area(
        "Enter text:",
        "What would you like to know about the bees today?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        images, answer = generate_response(question)
        st.write("Question: ", question)
        if isinstance(answer, dict):
            st.write("These are the images: ", images)
            if images:
                for image in images:
                    st.image(image, caption="Bee Image")
            if 'text' in answer:
                st.write("Answer: ", answer['text'])
        else:
            st.write("Answer: ", answer)
            if images:
                for image in images:
                    st.write("These are the images: ", image[0])
                    st.image(image[0], caption="Figure Number: " + str(image[1]))
                    