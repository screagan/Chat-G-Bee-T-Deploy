from scripts.vectorstore.figures.BOTW.getContextForBOTWFigureDescriptions import get_context_for_BOTW_figure_descriptions
from scripts.utils.client_provider import ClientProvider
# Read in MMD text files, generated with standardizeMMDFigureReferences.py
import pandas as pd

def generate_descriptions_of_BOTW_figures():

    # Read CSVs into DataFrames
    main_text_chunks_df = pd.read_csv("data/dataframesForEmbeddings/short_test_botw_text_chunks.csv", encoding="utf-8")
    keys_text_chunks_df = pd.read_csv("data/dataframesForEmbeddings/botw_keys_chunks.csv", encoding="utf-8")

    # Process the DataFrames
    context_df = get_context_for_BOTW_figure_descriptions(main_text_chunks_df, keys_text_chunks_df)

    openai_client = ClientProvider.get_openai_client()

    # Generate descriptions for each figure using the function below, add them to dataframe
    context_df['Image Description'] = context_df.apply(lambda row: generate_figure_description(openai_client, row['Figure Number'], row['Context']), axis=1)
    
    # Remove the 'Context' column from the DataFrame
    descriptions_df = context_df.drop(columns=['Context'])
    return descriptions_df


#Function to takes in context (figure references) of a figure and creates a description.
#We will embed these descriptions rather than embedding the image themselves.
def generate_figure_description(client, figure_num, context):
    """
    Calls OpenAI's API to generate a figure description optimized for embedding retrieval.

    Args:
    - figure_num (str): Figure number in the format (Fig. X).
    - context (str): Context related to the figure, as well as some surrounding figures (e.g., labels, features, or extracted text).

    Returns:
    - str: Generated description.
    """
    prompt = f"""
    Generate a **figure description** of Fig. {figure_num} optimized for embedding retrieval.
    - Summarize the **main topic of the figure** in the first sentence.
    - Ignore information about any figures that are not Fig. {figure_num}
    - Clearly describe the **key labeled components** and their significance.
    - Avoid excessive detail that is obvious from viewing the image.
    - Keep it **concise (100-200 words) and semantically rich** for retrieval.
    - Ensure it's **self-contained** (no reliance on external text).

    Context: {context}
    """
    #TODO: CONSIDER FEW SHOT LEARNING
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert at generating precise and informative descriptions of scientific and technical figures."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3  # Keeps responses precise and factual
    )

    print(f"Created a description for Fig. {figure_num}")
    return response.choices[0].message.content