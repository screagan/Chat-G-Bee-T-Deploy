from openai import OpenAI
from text.extractTextFromPDF import extract_text_from_pdf
from figures.MMD.standardizeFigRefsFromText import standardize_figures
from figures.MMD.getContextForMMDFigures import get_context_for_MMD_figure_descriptions
from dotenv import load_dotenv
import os

def generate_descriptions_of_MMD_figures():

    bucket_name = "ccber-tester-bucket"
    object_key_1 = "MMD-Main-Text.pdf"
    main_text = extract_text_from_pdf(object_key_1, bucket_name)
    main_text = standardize_figures(main_text)

    object_key_2 =  "MMD-Keys.pdf"
    keys_text = extract_text_from_pdf(object_key_2, bucket_name)
    keys_text = standardize_figures(keys_text)

    context_df = get_context_for_MMD_figure_descriptions(main_text, keys_text)

    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)
    context_df['Generated Description'] = context_df.apply(lambda row: generate_figure_description(client, row['Figure'], row['Context']), axis=1)
    return context_df


#Function to take in OpenAI client, figure number, and figure context, and generate a description
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
