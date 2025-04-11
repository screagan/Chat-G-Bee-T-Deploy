import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text_to_dataframe(text, source_name):
    # Initialize the text chunker
    custom_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=30,
        length_function=len
    )

    # Chunk the text
    chunks = custom_text_splitter.create_documents([text])

    # Extract chunk data
    data = []
    for idx, chunk in enumerate(chunks[:200]):
        data.append({
            'Source': source_name,
            'Type': 'Text',
            'Text Content': chunk.page_content,
            'Figure Number': 'NA',
            'Image Key': 'NA',
            'Image URL': 'NA',
            'Image Description': 'NA',
        })


    # Create and return DataFrame
    return pd.DataFrame(data)