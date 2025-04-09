import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text_to_dataframe(text, source):
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
            "chunk_id": f"{source}_CHUNK_{idx}",
            "chunk_text": chunk.page_content,
            "source": f"{source}"
        })

    # Create and return DataFrame
    return pd.DataFrame(data)