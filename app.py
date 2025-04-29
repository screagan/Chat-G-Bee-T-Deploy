

from scripts.vectorstore.text.chunkText import chunk_text_to_dataframe
from scripts.vectorstore.text.extractTextFromPDF import extract_text_from_pdf 
from scripts.vectorstore.figures.MMD.MMDFigureDescriptions import generate_descriptions_of_MMD_figures

if __name__ == "__main__":
    # # Example Usage
    # question = input("Ask me a question: ")
    # retrieval_results = retrieve_relevant_data(question)
    # answer = generate_answer_with_images(question, retrieval_results)

    # print(answer)  # Displays the OpenAI-generated response

  

    # import pandas as pd

# First: Get text chunks from main text of MMD, put them into DF ready to be embedded
# with open("data/MMD-Main-Text-Original.txt", "r", encoding="utf-8") as f:
#      mmd_main_text = f.read()

#     mmd_extracted_texts = extract_text_from_pdf(object_key='MMD-Main-Text.pdf', bucket_name='ccber-tester-bucket')
    
# # Create DataFrame with chunks and page numbers
#     mmd_text_chunks_df = chunk_text_to_dataframe(extracted_texts=mmd_extracted_texts, source_name="MMD")

#     mmd_text_chunks_df.to_csv("data/mmd_text_chunks.csv", index=False)
#     print(list(mmd_text_chunks_df.columns))

    mmd_figs_df = generate_descriptions_of_MMD_figures()
    mmd_figs_df.to_csv("data/mmd_figs.csv", index=False)
    print(list(mmd_figs_df.columns))    