from scripts.vectorstore.figures.hymenoptera.generateDescriptionsOfHOTWFigures import generate_descriptions_of_HOTW_figures
from scripts.vectorstore.figures.MMD.generateDescriptionsOfMMDFigures import generate_descriptions_of_MMD_figures
from scripts.vectorstore.text.chunkMainTextAndPutIntoDataframe import chunk_main_text_and_put_into_dataframe
from scripts.vectorstore.text.extractTextFromPDF import extract_text_from_pdf   
import pandas as pd

if __name__ == "__main__":

# Get text chunks and page numbers from main text of MMD, put them into DF ready to be embedded
# We do not use text chunks from the keys text of MMD, because it is not useful for embeddings
# The information within the keys text of MMD is accessible to the chatbots through figure descriptions
    mmd_extracted_main_text = extract_text_from_pdf(object_key='MMD-Main-Text.pdf', bucket_name='ccber-tester-bucket', num_columns=1)
    mmd_text_chunks_df = chunk_main_text_and_put_into_dataframe(extracted_texts=mmd_extracted_main_text, source_title='MMD', source_year='2022', source_author='Danforth, Bryan, et al.', source_publisher='MMDPublisher')
    mmd_text_chunks_df.to_csv("data/dataframesForEmbeddings/mmd_text_chunks.csv", index=False) #Save to csv to check out chunks. Optional.
    print("Made text chunks for MMD")

# Generate descriptions of MMD Figures, put them into DF ready to be embedded
    mmd_figs_df = generate_descriptions_of_MMD_figures()
    mmd_figs_df.to_csv("data/dataframesForEmbeddings/mmd_figs.csv", index=False)
    print(list(mmd_figs_df.columns))

# Get text chunks and page numbers from HOTW, put them into DF ready to be embedded
# Like MMD, we do not use text chunks from the keys text of HOTW, all of that info is in the figure descriptions
    hymenoptera_extracted_main_text = extract_text_from_pdf(object_key='HOTW-Main-Text.pdf', bucket_name='ccber-tester-bucket', num_columns=2) #TODO: This pdf is kinda off center. Check text extraction.
    hymenoptera_text_chunks_df = chunk_main_text_and_put_into_dataframe(extracted_texts=hymenoptera_extracted_main_text, source_title="Hymenoptera of the World", source_year='1993', source_author='Charles D. Michener', source_publisher='HOTWPublisher')
    hymenoptera_text_chunks_df.to_csv("data/dataframesForEmbeddings/hymenoptera_text_chunks.csv", index=False)
    print("Made text chunks for HOTW")

# Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded
    hymenoptera_figs_df = generate_descriptions_of_HOTW_figures()
    hymenoptera_figs_df.to_csv("data/dataframesForEmbeddings/hymenoptera_figs.csv", index=False)
    print(list(hymenoptera_figs_df.columns))

# Get text chunks and page numbers from BOTW, put them into DF ready to be embedded 
# TODO: Get full main text only, right now you just have small sample pages instead of proper entirety of main text.
    botw_extracted_main_text = extract_text_from_pdf(object_key='short_BOTW_Main_Text.pdf', bucket_name='ccber-tester-bucket', num_columns=2)
    botw_text_chunks_df = chunk_main_text_and_put_into_dataframe(extracted_texts=botw_extracted_main_text, source_title="Bees of the World", source_year='2007', source_author='Daniel C. Danforth', source_publisher='BOTWPublisher')
    botw_text_chunks_df.to_csv("data/dataframesForEmbeddings/short_test_botw_text_chunks.csv", index=False)
    print("Made text chunks for (shorter version of) BOTW")

# TODO: Add an BOTW keys chunk section, because unlike MMD and HOTW, BOTW has a keys section that is useful for embeddings.

# Generate descriptions of BOTW Figures, put them into DF ready to be embedded 
    # botw_figs_df = TODO: Make this function actually work to make figure descriptions for BOTW
    # botw_figs_df.to_csv("data/dataframesForEmbeddings/botw_figs.csv", index=False)
    # print(list(botw_figs_df.columns))

# Combine all DataFrames into a single DataFrame
    combined_df = pd.concat([mmd_text_chunks_df, mmd_figs_df, hymenoptera_text_chunks_df, hymenoptera_figs_df, botw_text_chunks_df], ignore_index=True)

# Save the combined DataFrame to a single CSV file
    combined_df.to_csv("data/dataframesForEmbeddings/combined_data.csv", index=False)
    print("Combined DataFrame saved to 'data/combined_data.csv'")

