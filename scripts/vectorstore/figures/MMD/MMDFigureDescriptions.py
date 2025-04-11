from openai import OpenAI
from figures.MMD.getContextForMMDFigures import get_context_for_MMD_figure_descriptions
from dotenv import load_dotenv
import os

def generate_descriptions_of_MMD_figures():

    # Read in MMD text files, already standardized references to figures (see standardizeFigRefsFromText.py in data folder)
    with open("data/MMD-Main-Text-With-Standardized-Fig-Refs.txt", "r", encoding="utf-8") as f:
     main_text = f.read()

    with open("data/MMD-Keys-With-Standardized-Fig-Refs.txt", "r", encoding="utf-8") as f:
     keys_text = f.read()

    # This function gathers all references to figures in the text, and returns a dataframe with the figure number, the context of the figure, and the s3 key for the figure
    # The context is the text surrounding the figure reference, and the s3 key is the location of the figure in our s3 bucket
    context_df = get_context_for_MMD_figure_descriptions(main_text, keys_text)

    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # Generate descriptions for each figure using the function below, add them to dataframe
    context_df['Description'] = context_df.apply(lambda row: generate_figure_description(client, row['Figure Number'], row['Context']), axis=1)
    
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
