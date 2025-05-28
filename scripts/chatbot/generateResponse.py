from  scripts.utils.client_provider import ClientProvider

def generate_response(query, retrieval_results, history):
    """
    Generates an answer using OpenAI API based on retrieved embeddings from Qdrant,
    considering conversation history.

    Args:
        query (str): The user's question.
        retrieval_results (list): The output of the Qdrant query (list of ScoredPoint objects).
        history (list): Previous conversation messages.

    Returns:
        tuple: (images_to_render, generated_answer)
    """

    # Extract text and figures into a cohesive context
    contexts = []
    images_to_render = []

    for result in retrieval_results:
        payload = result.payload
        content_type = payload.get("content_type")
        
        if content_type == "image_description":
            figure_number = payload.get("figure_number")
            description = payload.get("image_description")
            image_url = payload.get("image_url")
            
            if description and figure_number:
                contexts.append(f"{description} (as seen in Figure {figure_number})")
            
            if image_url:
                images_to_render.append((image_url, figure_number))
                
        elif content_type == "text_chunk":
            text_content = payload.get("text_content")
            if text_content:
                contexts.append(text_content)

    # Display images for reference
    if images_to_render:
        print("Image URLs for reference:")
        for url, fig_num in images_to_render:
            print(f"Figure {fig_num}: {url}")

    # Format conversation history for the prompt
    conversation_context = ""
    if history:
        conversation_context = "Previous conversation:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            # Only include the text content, not image references
            conversation_context += f"{role}: {msg['content']}\n"

    # Construct OpenAI Prompt
    prompt = f"""
    You are a scientific assistant helping to answer questions about bees using retrieved figure descriptions and text.

    {conversation_context}

    **Current User Question:** {query}

    **Relevant Information:** {' '.join(contexts) if contexts else 'No relevant information found.'}

    **Instructions:**
    - Answer the question directly in a clear and concise manner.
    - If figures are available, reference them naturally within the response (e.g., "as shown in Figure 3").
    - Do not list figures separately; integrate them passively in the explanation.
    - Consider the previous conversation for context when crafting your response.
    - Maintain a coherent conversation flow by referring to previously discussed topics if relevant.
    - If specific figures are mentioned in the text, reference them properly.
    - If the question is not answerable with the provided information, politely inform the user.
    - If the question is outside your expertise, suggest consulting a specialist or provide a general answer.
    - If the question is too vague, ask for clarification.
    - If there are no sources available, inform the user that you cannot provide an answer.
    """

    client = ClientProvider.get_openai_client()
    
    # Call OpenAI API with conversation history context
    stream = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert assistant that analyzes images and text to answer scientific questions about bees. Maintain context from the ongoing conversation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        stream=True
    )

    return images_to_render, stream

