from figures.hymenoptera.hymenopteraFigureDescriptions import generate_descriptions_of_hymenoptera_figures
from figures.MMD.MMDFigureDescriptions import generate_descriptions_of_MMD_figures
from text.chunkText import chunk_text_to_dataframe
from text.extractTextFromPDF import extract_text_from_pdf   

import pandas as pd

if __name__ == "__main__":

    # import pandas as pd
# Get text chunks and page numbers from main text of MMD, put them into DF ready to be embedded
    mmd_extracted_texts = extract_text_from_pdf(object_key='MMD-Main-Text.pdf', bucket_name='ccber-tester-bucket')
    mmd_text_chunks_df = chunk_text_to_dataframe(extracted_texts=mmd_extracted_texts, source_name="MMD")
    mmd_text_chunks_df.to_csv("data/dataframesForEmbeddings/mmd_text_chunks.csv", index=False) #Save to csv to check out chunks. Optional.
    print("Made text chunks for MMD")

# Generate descriptions of MMD Figures, put them into DF ready to be embedded
    mmd_figs_df = generate_descriptions_of_MMD_figures()
    mmd_figs_df.to_csv("data/dataframesForEmbeddings/mmd_figs.csv", index=False)
    print(list(mmd_figs_df.columns))

# Get text chunks and page numbers from HOTW, put them into DF ready to be embedded #TODO: Maybe edit which pages of HOTW text I upload
    hymenoptera_extracted_texts = extract_text_from_pdf(object_key='Hymenoptera_of_the_work.pdf', bucket_name='ccber-tester-bucket')
    hymenoptera_text_chunks_df = chunk_text_to_dataframe(extracted_texts=hymenoptera_extracted_texts, source_name="Hymenoptera of the World")
    hymenoptera_text_chunks_df.to_csv("data/dataframesForEmbeddings/hymenoptera_text_chunks.csv", index=False)
    print("Made text chunks for HOTW")

# Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded
    hymenoptera_figs_df = generate_descriptions_of_hymenoptera_figures()
    hymenoptera_figs_df.to_csv("data/dataframesForEmbeddings/hymenoptera_figs.csv", index=False)
    print(list(hymenoptera_figs_df.columns))

# Get text chunks and page numbers from BOTW, put them into DF ready to be embedded 
# TODO: Talk to project managers / Daniel and see how we should get this text.
    # botw_extracted_texts = extract_text_from_pdf(object_key='Bees_of_the_World.pdf', bucket_name='ccber-tester-bucket')
    # botw_text_chunks_df = chunk_text_to_dataframe(extracted_texts=botw_extracted_texts, source_name="Bees of the World")
    # botw_text_chunks_df.to_csv("data/dataframesForEmbeddings/botw_text_chunks.csv", index=False)
    # print("Made text chunks for BOTW")

# Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded 
    # botw_figs_df = TODO: Make this function actually work to make figure descriptions for BOTW
    # botw_figs_df.to_csv("data/dataframesForEmbeddings/botw_figs.csv", index=False)
    # print(list(botw_figs_df.columns))

# Combine all DataFrames into a single DataFrame
    combined_df = pd.concat([mmd_text_chunks_df, mmd_figs_df, hymenoptera_text_chunks_df, hymenoptera_figs_df], ignore_index=True)

# Save the combined DataFrame to a single CSV file
    combined_df.to_csv("data/dataframesForEmbeddings/combined_data.csv", index=False)
    print("Combined DataFrame saved to 'data/combined_data.csv'")

