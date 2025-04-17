
import textwrap
import requests
from PIL import Image
from io import BytesIO
import time
from  scripts.utils.client_provider import ClientProvider

def generate_answer_with_images(query, retrieval_results):
    """
    Generates an answer using OpenAI API based on retrieved embeddings from Qdrant.
    Mentions figures passively instead of listing them separately.

    Args:
        client (OpenAI): The OpenAI client.
        query (str): The user's question.
        retrieval_results (list): The output of the Qdrant query (list of ScoredPoint objects).

    Returns:
        str: The generated answer from OpenAI.
    """

    # Extract text and figures into a cohesive context
    contexts = []
    images_to_render = []

    for result in retrieval_results:
        payload = result.payload
        content_type = payload.get("content_type")
        
        if content_type == "image_description":
            # Handle image descriptions
            figure_number = payload.get("figure_number")
            description = payload.get("image_description")
            image_url = payload.get("image_url")
            
            if description and figure_number:
                contexts.append(f"{description} (as seen in Figure {figure_number})")
            
            if image_url:
                images_to_render.append((image_url, figure_number))
                
        elif content_type == "text_chunk":
            # Handle text chunks
            text_content = payload.get("text_content")
            if text_content:
                contexts.append(text_content)

    # Display images (choose one of these options)
    if images_to_render:
        # Option 1: Show images using PIL (for local display)
        # display_images_pil(images_to_render)
        
        # Option 2: Just print the image URLs for reference
        print("Image URLs for reference:")
        for url, fig_num in images_to_render:
            print(f"Figure {fig_num}: {url}")

    # Construct OpenAI Prompt
    prompt = f"""
    You are a scientific assistant helping to answer questions using retrieved figure descriptions and text.

    **User Question:** {query}

    **Relevant Information:** {' '.join(contexts) if contexts else 'No relevant information found.'}

    **Instructions:**
    - Answer the question directly in a clear and concise manner.
    - If figures are available, reference them naturally within the response (e.g., "as shown in Figure 3").
    - Do not list figures separately; integrate them passively in the explanation.
    - If specific figures are mentioned in the text, reference them properly.
    """

    client = ClientProvider.get_openai_client()
    # Call OpenAI API  
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are an expert assistant that analyzes images and text to answer scientific questions."},
                  {"role": "user", "content": prompt}],
        temperature=0.3
    )

    return images_to_render, textwrap.fill(response.choices[0].message.content, width=80)

def display_images_pil(image_urls):
    """Display images using PIL"""
    for url, fig_num in image_urls:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            print(f"\nDisplaying Figure {fig_num}:")
            img.show()  # This will open the image in the default image viewer
            time.sleep(1)  # Give some time for the image viewer to open
        except Exception as e:
            print(f"Could not display image from {url}: {e}")

