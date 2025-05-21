from scripts.utils.client_provider import ClientProvider
from ..getFiguresFromAWS import get_figures_from_AWS
import os

# We need to generate captions for our figures in the hymenoptera data source.
# This works well for figures which have a caption within view of the figure.

def generate_descriptions_of_HOTW_figures():

    # Create OpenAI Client
    openai_client = ClientProvider.get_openai_client()

    # Get dataframe containing figures from Hymenoptera
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    figures_df = get_figures_from_AWS(
        bucket_name=bucket_name,
        aws_folder='HOTW-Figures/',
        source_title="Hymenoptera of the World",
        source_year='1993',
        source_author='John I Huber',
        source_publisher='HOTWPublisher'
    )

    descriptions = []

    for i, row in figures_df.iterrows():
        url = row["Image URL"]
        figure_num = row["Figure Number"] if "Figure Number" in row else f"{i+1}"
        source = "Hymenoptera of the World (1993)"
        author = "Charles D. Michener"
        # Construct your custom prompt
        prompt = f"""
        Generate a **figure description** of Fig. {figure_num} optimized for embedding retrieval.
        - Mention the figure number, source ({source}) and author ({author}) in the first sentence. 
        - Mention the figure number and source in the first sentence. 
        - Summarize the **main topic of the figure** in the first sentence.
        - Clearly describe the **key labeled components** and their significance.
        - Keep it **concise (100-200 words) and semantically rich** for retrieval.
        - Ensure it's **self-contained** (no reliance on external text).
        """

        try:
            # Send the prompt and image to OpenAI
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": url,
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )
            description = response.choices[0].message.content
        except Exception as e:
            description = f"Error: {str(e)}"

        print("Created description for image:", url)
        descriptions.append(description)

    # Add descriptions to dataframe
    figures_df["Image Description"] = descriptions

    return figures_df


        

