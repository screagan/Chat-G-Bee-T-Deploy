import os
import uuid
import pandas as pd
import numpy as np
from tqdm import tqdm
from qdrant_client import models as rest
from concurrent.futures import ThreadPoolExecutor, as_completed
from scripts.utils.client_provider import ClientProvider
import threading

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
BATCH_SIZE = 500  # Increased batch size
MAX_WORKERS = 4   # For parallel embedding generation

qdrant_client = ClientProvider.get_qdrant_client()
embeddings = ClientProvider.get_embeddings()

def create_collection_if_not_exists(collection_name, vector_size=1536):
    """Create collection if it doesn't exist"""
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists with {collection_info.vectors_count} points.")
        return True
    except Exception:
        print(f"Creating collection '{collection_name}'...")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(
                size=vector_size,
                distance=rest.Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created successfully!")
        return True

def prepare_content_for_embedding(df):
    """Pre-process and prepare content for embedding"""
    content_list = []
    valid_indices = []
    
    for idx, row in df.iterrows():
        if pd.notna(row['Text Content']) and row['Text Content'].strip():
            content_list.append(row['Text Content'].strip())
            valid_indices.append((idx, 'text_chunk'))
        elif pd.notna(row['Image Description']) and row['Image Description'].strip():
            content_list.append(row['Image Description'].strip())
            valid_indices.append((idx, 'image_description'))
        else:
            print(f"Warning: Row {idx} has no valid content to embed")
    
    return content_list, valid_indices

def generate_embeddings_batch(content_list, batch_size=50):
    """Generate embeddings in batches to optimize API calls"""
    embeddings_list = []
    
    # If your embedding provider supports batch processing, use it
    if hasattr(embeddings, 'embed_documents'):
        # Use batch embedding if available
        for i in tqdm(range(0, len(content_list), batch_size), desc="Generating embeddings"):
            batch_content = content_list[i:i + batch_size]
            batch_embeddings = embeddings.embed_documents(batch_content)
            embeddings_list.extend(batch_embeddings)
    else:
        # Fallback to individual embeddings with threading
        def embed_single(content):
            return embeddings.embed_query(content)
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_content = {executor.submit(embed_single, content): i 
                               for i, content in enumerate(content_list)}
            
            # Create list to maintain order
            embeddings_list = [None] * len(content_list)
            
            for future in tqdm(as_completed(future_to_content), 
                             total=len(content_list), desc="Generating embeddings"):
                idx = future_to_content[future]
                try:
                    embeddings_list[idx] = future.result()
                except Exception as exc:
                    print(f'Embedding generation failed for content {idx}: {exc}')
    
    return embeddings_list

def create_point_from_row(row, embedding_vector, content_type, point_id=None):
    """Create a Qdrant point from dataframe row"""
    if point_id is None:
        point_id = str(uuid.uuid4())
    
    # Optimize payload - only include non-null/non-empty values
    payload = {"content_type": content_type}
    
    # Add fields only if they have meaningful values
    if pd.notna(row['Title']) and row['Title'].strip():
        payload["title"] = row['Title'].strip()
    if pd.notna(row['Year']) and row['Year'] != '':
        payload["year"] = str(row['Year'])
    if pd.notna(row['Author']) and row['Author'].strip():
        payload["author"] = row['Author'].strip()
    if pd.notna(row['Publisher']) and row['Publisher'].strip():
        payload["publisher"] = row['Publisher'].strip()
    if pd.notna(row['Page Number']):
        try:
            payload["page_number"] = int(float(row['Page Number']))
        except (ValueError, TypeError):
            pass
    if pd.notna(row['Type']) and row['Type'].strip():
        payload["type"] = row['Type'].strip()
    
    # Content-specific fields
    if content_type == 'text_chunk' and pd.notna(row['Text Content']):
        payload["text_content"] = row['Text Content'].strip()
    elif content_type == 'image_description':
        if pd.notna(row['Image Description']):
            payload["image_description"] = row['Image Description'].strip()
        if pd.notna(row['Figure Number']):
            payload["figure_number"] = str(row['Figure Number'])
        if pd.notna(row['Image Key']) and row['Image Key'].strip():
            payload["image_key"] = row['Image Key'].strip()
        if pd.notna(row['Image URL']) and row['Image URL'].strip():
            payload["image_url"] = row['Image URL'].strip()
    
    return rest.PointStruct(
        id=point_id,
        vector=embedding_vector,
        payload=payload
    )

def upload_to_qdrant_optimized(df):
    """Optimized upload to Qdrant with batch embedding generation"""
    
    # Create collection if needed
    create_collection_if_not_exists(COLLECTION_NAME)
    
    print(f"Processing {len(df)} records...")
    
    # Step 1: Prepare content for embedding
    content_list, valid_indices = prepare_content_for_embedding(df)
    
    if not content_list:
        print("No valid content found for embedding!")
        return
    
    print(f"Found {len(content_list)} valid records for embedding...")
    
    # Step 2: Generate all embeddings at once (most efficient)
    embeddings_list = generate_embeddings_batch(content_list)
    
    if len(embeddings_list) != len(valid_indices):
        print("Error: Mismatch between embeddings and valid indices!")
        return
    
    # Step 3: Upload to Qdrant in batches
    total_points = 0
    points_batch = []
    
    for i, (embedding_vector, (row_idx, content_type)) in enumerate(
        tqdm(zip(embeddings_list, valid_indices), desc="Preparing points")
    ):
        row = df.iloc[row_idx]
        point = create_point_from_row(row, embedding_vector, content_type)
        points_batch.append(point)
        
        # Upload when batch is full or at the end
        if len(points_batch) >= BATCH_SIZE or i == len(embeddings_list) - 1:
            try:
                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points_batch,
                    wait=False  # Don't wait for indexing to complete
                )
                total_points += len(points_batch)
                print(f"Uploaded batch of {len(points_batch)} points. Total: {total_points}")
                points_batch = []
            except Exception as e:
                print(f"Error uploading batch: {e}")
                # You might want to retry logic here
    
    print(f"Upload complete! {total_points} points uploaded successfully.")

def verify_upload():
    """Verify the upload by counting points in collection"""
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' contains {collection_info.vectors_count} points.")
        
        # Sample a few points to verify structure
        search_result = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        
        print("Sample points:")
        for point in search_result[0]:
            print(f"ID: {point.id}")
            print(f"Payload keys: {list(point.payload.keys())}")
            print("---")
            
    except Exception as e:
        print(f"Error during verification: {e}")

# Main execution
if __name__ == "__main__":
    # Load dataframe
    df = pd.read_csv('data/dataframesForEmbeddings/combined_data.csv')
    
    # Clean dataframe - remove completely empty rows
    df = df.dropna(how='all')
    
    # Upload data to Qdrant using optimized method
    upload_to_qdrant_optimized(df)
    
    # Verify the upload
    verify_upload()