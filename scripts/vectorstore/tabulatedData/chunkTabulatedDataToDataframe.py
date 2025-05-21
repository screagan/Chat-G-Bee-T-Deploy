import pandas as pd
import io
import re
from scripts.utils.client_provider import ClientProvider

def chunk_tabulated_data_to_dataframe(object_key, bucket_name, source_title, source_year, source_author, source_publisher):
    """
    Process bee data from an AWS S3 bucket based on the object key.
    
    Parameters:
    - object_key: One of "cleaned_database", "globi_bees", "discover_life", or "dori_bees"
    - bucket_name: The S3 bucket name
    - region_name: AWS region name
    - source_title, source_year, source_author, source_publisher: Metadata for the dataframe
    
    Returns:
    - DataFrame with processed data
    """
    # Initialize AWS client
    s3 = ClientProvider.get_s3_client()
    
    try:
        # Download the CSV file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        csv_content = response['Body'].read().decode('utf-8')
        
        # Process the content based on object_key
        if object_key == "discover_life.txt":
            # Split at "The scientific name of this bee is..."
            chunks = re.split(r'The scientific name of this bee is', csv_content)
            # Add back the split text to each chunk except the first
            chunks = [chunks[0]] + [f"The scientific name of this bee is{chunk}" for chunk in chunks[1:]]
        
        elif object_key == "dori_bees.txt":
            # Split at "The canonical name of this bee..."
            chunks = re.split(r'The canonical name of this bee', csv_content)
            # Add back the split text to each chunk except the first
            chunks = [chunks[0]] + [f"The canonical name of this bee{chunk}" for chunk in chunks[1:]]
        
        elif object_key == "cleaned_database.pdf":
            # Split at "==="
            chunks = re.split(r'===', csv_content)
        
        # elif object_key == "globi_bees": TODO: figure out how to split globi_bees

        
        else:
            raise ValueError(f"Invalid object_key: {object_key}. Expected one of 'cleaned_database', 'globi_bees', 'discover_life', or 'dori_bees'")
        
        # Create a list to hold our data
        data = []
        
        # Process each chunk and add to data list
        for i, chunk in enumerate(chunks):
            # Skip empty chunks
            if not chunk.strip():
                continue
                
            data.append({
                'Title': source_title,
                'Year': source_year,
                'Author': source_author,
                'Publisher': source_publisher,
                'Page Number': 'NA',  # Use chunk index as page number
                'Type': 'Tabulated Data',
                'Text Content': chunk.strip(),
                'Figure Number': 'NA',
                'Image Key': 'NA',
                'Image URL': 'NA',
                'Image Description': 'NA',
            })
        
        # Create and return DataFrame
        return pd.DataFrame(data)
    
    except Exception as e:
        print(f"Error processing {object_key}: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error