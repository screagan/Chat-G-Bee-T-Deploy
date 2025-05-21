from scripts.vectorstore.figures.hymenoptera.generateDescriptionsOfHOTWFigures import generate_descriptions_of_HOTW_figures
from scripts.vectorstore.figures.MMD.generateDescriptionsOfMMDFigures import generate_descriptions_of_MMD_figures
from scripts.vectorstore.text.chunkMainTextAndPutIntoDataframe import chunk_main_text_and_put_into_dataframe
from scripts.vectorstore.text.extractTextFromPDF import extract_text_from_pdf   
from scripts.vectorstore.figures.BOTW.generateDescriptionsOfBOTWFigures import generate_descriptions_of_BOTW_figures
from scripts.vectorstore.text.chunkBOTWKeysAndPutIntoDataframe import chunk_BOTW_keys_and_put_into_dataframe
from scripts.vectorstore.tabulatedData.chunkTabulatedDataToDataframe import chunk_tabulated_data_to_dataframe
import pandas as pd

#If you want to do testing and you already have the dataframes, you can make a sample below
def create_sample_dataframes():
    # Create individual sample dataframes
    mmd_text_sample = mmd_text_chunks_df.head(5)
    mmd_figs_sample = mmd_figs_df.head(5)
    hymenoptera_text_sample = hymenoptera_text_chunks_df.head(5)
    hymenoptera_figs_sample = hymenoptera_figs_df.head(5)
    botw_text_sample = botw_text_chunks_df.head(5)
    botw_keys_sample = botw_keys_chunks_df.head(5)
    botw_figs_sample = botw_figs_df.head(5)
    discover_life_sample = discover_life_df.head(5)
    dori_bees_sample = dori_bees_df.head(5)
    
    # Save individual samples
    mmd_text_sample.to_csv("data/sample_dataframes/mmd_text_chunks_sample.csv", index=False)
    mmd_figs_sample.to_csv("data/sample_dataframes/mmd_figs_sample.csv", index=False)
    hymenoptera_text_sample.to_csv("data/sample_dataframes/hymenoptera_text_chunks_sample.csv", index=False)
    hymenoptera_figs_sample.to_csv("data/sample_dataframes/hymenoptera_figs_sample.csv", index=False)
    botw_text_sample.to_csv("data/sample_dataframes/botw_text_chunks_sample.csv", index=False)
    botw_keys_sample.to_csv("data/sample_dataframes/botw_keys_chunks_sample.csv", index=False)
    botw_figs_sample.to_csv("data/sample_dataframes/botw_figs_sample.csv", index=False)
    discover_life_sample.to_csv("data/sample_dataframes/discover_life_chunks_sample.csv", index=False)
    dori_bees_sample.to_csv("data/sample_dataframes/dori_bees_chunks_sample.csv", index=False)
    
    
    # Create a list of all sample dataframes
    sample_dfs = [
        mmd_text_sample,
        mmd_figs_sample,
        hymenoptera_text_sample,
        hymenoptera_figs_sample,
        botw_text_sample,
        botw_keys_sample,
        botw_figs_sample,
        discover_life_sample,
        dori_bees_sample
    ]
    
    # Check if all dataframes have the same columns
    # If not, we'll need to use concat with ignore_index=True
    # This will preserve all columns but may result in NaN values
    combined_samples = pd.concat(sample_dfs, ignore_index=True)
    
    # Save the combined dataframe
    combined_samples.to_csv("data/sample_dataframes/combined_samples.csv", index=False)
    
    print("Created individual sample dataframes and a combined sample dataframe")
    print(f"Combined sample shape: {combined_samples.shape}")
    
    return combined_samples


if __name__ == "__main__":

# Get text chunks and page numbers from main text of MMD, put them into DF ready to be embedded
# We do not use text chunks from the keys text of MMD, because it is not useful for embeddings
# The information within the keys text of MMD is accessible to the chatbots through figure descriptions
    # mmd_extracted_main_text = extract_text_from_pdf(object_key='MMD-Main-Text.pdf', bucket_name='ccber-tester-bucket', num_columns=1)
    # mmd_text_chunks_df = chunk_main_text_and_put_into_dataframe(extracted_texts=mmd_extracted_main_text, source_title='MMD', source_year='2022', source_author='Danforth, Bryan, et al.', source_publisher='MMDPublisher')
    # mmd_text_chunks_df.to_csv("data/dataframesForEmbeddings/mmd_text_chunks.csv", index=False) #Save to csv to check out chunks. Optional.
    # print("Made text chunks for MMD")

# Generate descriptions of MMD Figures, put them into DF ready to be embedded
    # mmd_figs_df = generate_descriptions_of_MMD_figures()
    # mmd_figs_df.to_csv("data/dataframesForEmbeddings/mmd_figs.csv", index=False)
    # print(list(mmd_figs_df.columns))

# Get text chunks and page numbers from HOTW, put them into DF ready to be embedded
# Like MMD, we do not use text chunks from the keys text of HOTW, all of that info is in the figure descriptions
    # hymenoptera_extracted_main_text = extract_text_from_pdf(object_key='HOTW-Main-Text.pdf', bucket_name='ccber-tester-bucket', num_columns=2) #TODO: This pdf is kinda off center. Check text extraction.
    # hymenoptera_text_chunks_df = chunk_main_text_and_put_into_dataframe(extracted_texts=hymenoptera_extracted_main_text, source_title="Hymenoptera of the World", source_year='1993', source_author='Charles D. Michener', source_publisher='HOTWPublisher')
    # hymenoptera_text_chunks_df.to_csv("data/dataframesForEmbeddings/hymenoptera_text_chunks.csv", index=False)
    # print("Made text chunks for HOTW")

# Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded
    # hymenoptera_figs_df = generate_descriptions_of_HOTW_figures()
    # hymenoptera_figs_df.to_csv("data/dataframesForEmbeddings/hymenoptera_figs.csv", index=False)
    # print(list(hymenoptera_figs_df.columns))

# Get text chunks and page numbers from BOTW, put them into DF ready to be embedded
    # botw_extracted_main_text = extract_text_from_pdf(object_key='BOTW-Main-Text.pdf', bucket_name='ccber-tester-bucket', num_columns=2)
    # botw_text_chunks_df = chunk_main_text_and_put_into_dataframe(extracted_texts=botw_extracted_main_text, source_title="Bees of the World", source_year='2007', source_author='Daniel C. Danforth', source_publisher='BOTWPublisher')
    # botw_text_chunks_df.to_csv("data/dataframesForEmbeddings/botw_text_chunks.csv", index=False)
    # print("Made text chunks for (shorter version of) BOTW")

# Unlike MMD and HOTW, BOTW has a keys section that is useful for embeddings, so we get information from it.
# This function does not extract the keys directly from the PDF, but rather gets the keys info from a text file created by Daniel based off of the keys (data/texts/bees-of-the-world-key-descriptions.txt)
    # botw_keys_chunks_df = chunk_BOTW_keys_and_put_into_dataframe()
    # botw_keys_chunks_df.to_csv("data/dataframesForEmbeddings/botw_keys_chunks.csv", index=False)
    # print("Made text chunks for BOTW keys")

# Generate descriptions of BOTW Figures using references in main text and keys, put them into DF ready to be embedded 
    # botw_figs_df = generate_descriptions_of_BOTW_figures()
    # botw_figs_df.to_csv("data/dataframesForEmbeddings/botw_figs.csv", index=False)
    # print(list(botw_figs_df.columns))

# Process bee data from additional sources and add to combined DataFrame
    # Process discover_life data
    # discover_life_df = chunk_tabulated_data_to_dataframe(object_key="discover_life.txt", bucket_name="ccber-tester-bucket", source_title="Discover Life Database", source_year="2025", source_author="Discover Life Research Team", source_publisher="Discover Life Publisher")
    # discover_life_df.to_csv("data/dataframesForEmbeddings/discover_life_chunks.csv", index=False)
    # print("Made text chunks for Discover Life")

    # Process dori_bees data
    # dori_bees_df = chunk_tabulated_data_to_dataframe( object_key="dori_bees.txt", bucket_name="ccber-tester-bucket", source_title="DORI Database", source_year="2025", source_author="DORI Research Team", source_publisher="DORI Publisher")
    # dori_bees_df.to_csv("data/dataframesForEmbeddings/dori_bees_chunks.csv", index=False)
    # print("Made text chunks for DORI Bees")

    # Process cleaned_database data 
    # TODO: Make it chunk_tabulated_data_to_dataframe() work with cleaned_database data

    # Process globi_bees data
    # TODO: Make it chunk_tabulated_data_to_dataframe() work with Globi bees data

# To instead read in previously generated CSV files, comment out the section above and uncomment the following lines:
    mmd_text_chunks_df = pd.read_csv("data/dataframesForEmbeddings/mmd_text_chunks.csv")
    mmd_figs_df = pd.read_csv("data/dataframesForEmbeddings/mmd_figs.csv")
    hymenoptera_text_chunks_df = pd.read_csv("data/dataframesForEmbeddings/hymenoptera_text_chunks.csv")
    hymenoptera_figs_df = pd.read_csv("data/dataframesForEmbeddings/hymenoptera_figs.csv")
    botw_text_chunks_df = pd.read_csv("data/dataframesForEmbeddings/botw_text_chunks.csv")
    botw_keys_chunks_df = pd.read_csv("data/dataframesForEmbeddings/botw_keys_chunks.csv")
    botw_figs_df = pd.read_csv("data/dataframesForEmbeddings/botw_figs.csv")
    discover_life_df = pd.read_csv("data/dataframesForEmbeddings/discover_life_chunks.csv")
    dori_bees_df = pd.read_csv("data/dataframesForEmbeddings/dori_bees_chunks.csv")
    # Don't uncomment, this does not work yet: cleaned_database_df = pd.read_csv("data/dataframesForEmbeddings/cleaned_database_chunks.csv")
    # Don't uncomment, this does not work yet: globi_bees_df = pd.read_csv("data/dataframesForEmbeddings/globi_bees_chunks.csv")

# To create a sample of the dataframes to test vectorstore uploading stuff, uncomment the following line:
    # create_sample_dataframes()

# Combine all DataFrames into a single DataFrame
    combined_df = pd.concat([mmd_text_chunks_df, mmd_figs_df, hymenoptera_text_chunks_df, hymenoptera_figs_df, botw_text_chunks_df, botw_keys_chunks_df, botw_figs_df, discover_life_df, dori_bees_df], ignore_index=True)

# Save the combined DataFrame to a single CSV file
    combined_df.to_csv("data/dataframesForEmbeddings/combined_data.csv", index=False)
    print("Combined DataFrame saved to 'data/combined_data.csv'")


