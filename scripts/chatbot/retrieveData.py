
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables (for API keys)
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")         
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")        
COLLECTION_NAME = "tester_ccber"             # Choose your collection name
BATCH_SIZE = 10                                     # Batch size for uploads

# Initialize clients
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def retrieve_relevant_data(query):

    test_embedding = embeddings.embed_query(query)
    search_results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=test_embedding,
        limit=5
    )
    
    for i, result in enumerate(search_results):
        print(f"Result {i+1}:")
        content_type = result.payload.get("content_type")
        if content_type == "text_chunk":
            print(f"- Text chunk: {result.payload.get('text_content')[:100]}...")
        else:
            print(f"- Image: Figure {result.payload.get('figure_number')}")
            print(f"- Description: {result.payload.get('image_description')[:100]}...")
        print(f"- Similarity score: {result.score}")
        print()

    return search_results