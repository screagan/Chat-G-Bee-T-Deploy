import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

# This function is meant specifically for chunking main text sections to dataframes
# This probably is not the method for chunkings keys text sections
def chunk_main_text_and_put_into_dataframe(extracted_texts, source_title, source_year, source_author, source_publisher):
    # Initialize the text splitter
    custom_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=30,
        length_function=len
    )
    
    data = []
    
    for page_item in extracted_texts:
        page_text = page_item['text']
        page_num = page_item['page_num']
        
        # Chunk the text for this page
        if page_text.strip():  # Only process non-empty text
            chunks = custom_text_splitter.create_documents([page_text])
            
            # Add chunks to data with page number
            for chunk in chunks:
                data.append({
                    'Title': source_title,
                    'Year': source_year,
                    'Author': source_author,
                    'Publisher': source_publisher,
                    'Page Number': page_num,  # Store the page number
                    'Type': 'Text',
                    'Text Content': chunk.page_content,
                    'Figure Number': 'NA',
                    'Image Key': 'NA',
                    'Image URL': 'NA',
                    'Image Description': 'NA',
                })
    
    # Create and return DataFrame
    return pd.DataFrame(data)