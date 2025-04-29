from figures.hymenoptera.hymenopteraFigureDescriptions import generate_descriptions_of_hymenoptera_figures
from figures.MMD.MMDFigureDescriptions import generate_descriptions_of_MMD_figures
from text.chunkText import chunk_text_to_dataframe
from text.extractTextFromPDF import extract_text_from_pdf   

import pandas as pd

if __name__ == "__main__":
    # # Example Usage
    # question = input("Ask me a question: ")
    # retrieval_results = retrieve_relevant_data(question)
    # answer = generate_answer_with_images(question, retrieval_results)

    # print(answer)  # Displays the OpenAI-generated response

    # import pandas as pd
# First: Get text chunks and page numbers from main text of MMD, put them into DF ready to be embedded
    mmd_extracted_texts = extract_text_from_pdf(object_key='MMD-Main-Text.pdf', bucket_name='ccber-tester-bucket')
    mmd_text_chunks_df = chunk_text_to_dataframe(extracted_texts=mmd_extracted_texts, source_name="MMD")

# Second: Get text chunks and page numbers from Hymenoptera, put them into DF ready to be embedded
# hymenoptera_extracted_texts = extract_text_from_pdf(object_key='Hymenoptera-Text', bucket_name='ccber-tester-bucket')
# hymenoptera_text_chunks_df = chunk_text_to_dataframe(extracted_texts=mmd_extracted_texts, source_name="Hymenoptera")

#Optional, save the DataFrames to a CSV file
# mmd_text_chunks_df.to_csv("data/mmd_text_chunks.csv", index=False)
# print(list(mmd_text_chunks_df.columns))

# mmd_text_chunks_df.to_csv("data/mmd_text_chunks.csv", index=False)
# print(list(mmd_text_chunks_df.columns))

# Third: Generate descriptions of MMD Figures, put them into DF ready to be embedded
    mmd_figs_df = generate_descriptions_of_MMD_figures()
    mmd_figs_df.to_csv("data/mmd_figs.csv", index=False)
    print(list(mmd_figs_df.columns))

# Fourth: Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded
    hymenoptera_figs_df = generate_descriptions_of_hymenoptera_figures()
    hymenoptera_figs_df.to_csv("data/hymenoptera_figs.csv", index=False)
    print(list(hymenoptera_figs_df.columns))

# Combine all DataFrames into a single DataFrame
    combined_df = pd.concat([mmd_text_chunks_df, mmd_figs_df, hymenoptera_figs_df], ignore_index=True)

# Save the combined DataFrame to a single CSV file
    combined_df.to_csv("data/combined_data.csv", index=False)
    print("Combined DataFrame saved to 'data/combined_data.csv'")

