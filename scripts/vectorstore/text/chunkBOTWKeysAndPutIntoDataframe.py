import pandas as pd

def chunk_BOTW_keys_and_put_into_dataframe(source_title="Bees Of The World", source_year='2007', source_author='Daniel C. Danforth', source_publisher='BOTWPublisher'):

    file_path = "data/texts/bees-of-the-world-key-descriptions.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        keys_text = f.read()

    data = []
    
    chunks = parse_and_chunk(keys_text)
            
    for chunk in chunks:
        data.append({
            'Title': source_title,
            'Year': source_year,
            'Author': source_author,
            'Publisher': source_publisher,
            'Page Number': 'NA' ,
            'Type': 'Text',
            'Text Content': chunk,
            'Figure Number': 'NA',
            'Image Key': 'NA',
            'Image URL': 'NA',
            'Image Description': 'NA',
        })
    
    # Create and return DataFrame
    return pd.DataFrame(data)

def parse_and_chunk(text):
    chunks = []
    families = text.split("=====")
    for family_block in families:
        if not family_block.strip():
            continue
        lines = family_block.strip().split("\n")
        header = lines[0].strip(":").strip()
        bullets = [line.strip("- ").strip() for line in lines[1:] if line.strip().startswith("-")]
        for bullet in bullets:
            chunks.append(f"{header}: {bullet}")
    print(chunks)
    return chunks
