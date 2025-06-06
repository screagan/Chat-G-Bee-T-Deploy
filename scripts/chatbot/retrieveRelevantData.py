
from scripts.utils.client_provider import ClientProvider
import os

def retrieve_relevant_data(query):

    qdrant_client = ClientProvider.get_qdrant_client()
    embeddings = ClientProvider.get_embeddings()
    COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

    # Create collection if it doesn't exist
    test_embedding = embeddings.embed_query(query)
    search_results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=test_embedding,
        limit=10,
        score_threshold=0.8
    )
    
    for i, result in enumerate(search_results):
        print(f"Result {i+1}:")
        content_type = result.payload.get("content_type")
        print(f"- Author: {result.payload.get('author')[:100]}...")
        if content_type == "text_chunk":
            print(f"- Text chunk: {result.payload.get('text_content')[:100]}...")
        else:
            print(f"- Image: Figure {result.payload.get('figure_number')}")
            print(f"- Description: {result.payload.get('image_description')[:100]}...")
        print(f"- Similarity score: {result.score}")
        print()

    return search_results