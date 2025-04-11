import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from langchain.embeddings import OpenAIEmbeddings
from tqdm.auto import tqdm
import uuid
import os
from dotenv import load_dotenv

# Load environment variables (for API keys)
load_dotenv()

# Configuration
QDRANT_URL = "https://9c0688d2-2dbd-4087-a682-937bff353293.us-west-1-0.aws.cloud.qdrant.io:6333"  # Replace with your Qdrant Cloud URL
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")         # Store your API key in .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")         # Store your OpenAI key in .env file
COLLECTION_NAME = "tester_ccber"             # Choose your collection name
BATCH_SIZE = 10                                     # Batch size for uploads

# Initialize clients
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def create_collection_if_not_exists(collection_name, vector_size=1536):
    """Create collection if it doesn't exist"""
    collections = qdrant_client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if collection_name not in collection_names:
        print(f"Creating collection '{collection_name}'...")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(
                size=vector_size,
                distance=rest.Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created successfully!")
    else:
        print(f"Collection '{collection_name}' already exists.")

def upload_to_qdrant(df):
    """Upload data from dataframe to Qdrant"""
    
    # First create collection if needed
    create_collection_if_not_exists(COLLECTION_NAME)
    
    total_rows = len(df)
    print(f"Processing {total_rows} records...")
    
    # Process in batches
    for i in tqdm(range(0, total_rows, BATCH_SIZE)):
        batch_df = df.iloc[i:i + BATCH_SIZE]
        
        # Prepare points for this batch
        points = []
        
        for _, row in batch_df.iterrows():
            # Determine the content to embed based on type
            if pd.notna(row['Text Content']):
                content_to_embed = row['Text Content']
                content_type = 'text_chunk'
            elif pd.notna(row['Image Description']):
                content_to_embed = row['Image Description']
                content_type = 'image_description'
            else:
                print(f"Warning: Row has no content to embed: {row}")
                continue
                
            # Create embedding
            embedding_vector = embeddings.embed_query(content_to_embed)
            
            # Create point ID
            point_id = str(uuid.uuid4())
            
            # Create metadata payload
            payload = {
                "source": row['Source'] if pd.notna(row['Source']) else '',
                "type": row['Type'] if pd.notna(row['Type']) else '',
                "content_type": content_type,
                "text_content": row['Text Content'] if pd.notna(row['Text Content']) else '',
                # Store image-specific data when available
                "figure_number": int(row['Figure Number']) if pd.notna(row['Figure Number']) else None,
                "image_key": row['Image Key'] if pd.notna(row['Image Key']) else '',
                "image_url": row['Image URL'] if pd.notna(row['Image URL']) else '',
                "image_description": row['Image Description'] if pd.notna(row['Image Description']) else ''
            }
            
            # Add point to batch
            points.append(rest.PointStruct(
                id=point_id,
                vector=embedding_vector,
                payload=payload
            ))
        
        # Upload batch to Qdrant
        if points:
            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            print(f"Batch of {len(points)} points uploaded successfully!")
        else:
            print("No valid points in this batch.")
    
    print(f"Upload complete! {total_rows} records processed.")

def verify_upload():
    """Verify the upload by counting points in collection"""
    collection_info = qdrant_client.get_collection(COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' contains {collection_info.vectors_count} points.")

# Main execution
if __name__ == "__main__":
    # Load your dataframe - replace with your actual dataframe loading code
    # Example: df = pd.read_csv('your_data.csv')
    
    # For testing, let's create a small sample dataframe:
#     df = pd.read_csv('data/dataframesForEmbeddings/combined_data.csv')  # Replace with your actual file path
    
#     # Upload data to Qdrant
#     upload_to_qdrant(df)
    
#     # Verify the upload
#     verify_upload()
    
    # Test simple search
    test_query = "what part of the bee is the occipital sulcus?"  # Replace with an actual test query
    test_embedding = embeddings.embed_query(test_query)
    search_results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=test_embedding,
        limit=5
    )
    
    print("\nTest search results:")
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