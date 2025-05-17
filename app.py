import streamlit as st
from scripts.chatbot.generateResponse import generate_response
from scripts.chatbot.retrieveData import retrieve_relevant_data

import streamlit as st

# Initialize session state for conversation history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
st.title("ChatG🐝T: Your Bee Knowledge Assistant")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "images" in message and message["images"]:
            for image in message["images"]:
                st.image(image[0], caption=f"Figure Number: {image[1]}")

def answer_user_question(input_text, history):
    # Convert history to format suitable for context
    formatted_history = []
    for msg in history:
        formatted_history.append({"role": msg["role"], "content": msg["content"]})
    
    # Get retrieval results
    retrieval_results = retrieve_relevant_data(input_text)
    
    # Extract source information
    sources_info = []
    for result in retrieval_results:
        source_info = {
            "title": result.payload.get("title", "Unknown"),
            "author": result.payload.get("author", "Unknown Author"),
            "year": result.payload.get("year", "Unknown Year"),
            "publisher": result.payload.get("publisher", "Unknown Publisher"),
            "page_number": result.payload.get("page_number", "N/A"),
            "content_type": result.payload.get("content_type", "Unknown"),
            "figure_number": result.payload.get("figure_number", "N/A"),
            "score": result.score
        }
        sources_info.append(source_info)
    
    # Generate answer considering history
    images, stream = generate_response(input_text, retrieval_results, formatted_history)
    
    return images, stream, sources_info  # Return three values including sources_info

# User input area
user_input = st.chat_input("What would you like to know about the bees today?")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            images, answer_stream, sources_info = answer_user_question(user_input, st.session_state.messages)
            
            # Initialize an empty container for the message
            response_placeholder = st.empty()

            # Stream the response word by word
            full_response = ""
            
            for chunk in answer_stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response)
            
            # Display sources information in an expander
            with st.expander("Sources of Information"):
                st.write("This response is based on the following sources:")
                for i, source in enumerate(sources_info):
        
                    author = source['author']
                    year = source['year']
                    title = source['title']
                    publisher = source['publisher']
                    
                    # Add page information (APA uses p. or pp.)
                    page_info = f"(p. {source['page_number']})" if source['page_number'] != 'N/A' else ''
                    
                    # Format figure information if available
                    figure_info = f", Figure {source['figure_number']}" if source['figure_number'] != 'N/A' and source['figure_number'] else ''
                    
                    # Put it all together in APA format
                    apa_citation = f'**Source {i+1}:** {author} ({year}). *{title}*'
                    
                    # Add publisher if available
                    if publisher:
                        apa_citation += f". {publisher}"
                    
                    # Add page and figure info
                    if page_info:
                        apa_citation += f" {page_info}"
                    if figure_info:
                        apa_citation += f"{figure_info}"
                    
                    # Add period at the end if needed
                    if not apa_citation.endswith('.'):
                        apa_citation += '.'
                    
                    st.markdown(apa_citation)
                
            # Display images (after text)    
            if images:
                for image in images:
                    st.image(image[0], caption=f"Figure Number: {image[1]}")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response, 
        "images": images,
        "sources": sources_info  # Store sources info for future reference
    })
                    