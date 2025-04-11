from openai import OpenAI
from ..getFiguresFromAWS import get_figures_from_source
from dotenv import load_dotenv
import os


# We need to generate captions for our figures in the hymenoptera data source.
# This works well for figures which have a caption within view of the figure.

def generate_descriptions_of_hymenoptera_figures():

    #get openai api key and create client
    load_dotenv()
    openai_api_key = os.getenv("API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    #Get dataframe containing figures from hymenoptera
    figures_df = get_figures_from_source(bucket_name=bucket_name, source_name='Hymenoptera-Figures/') 
    
    descriptions = []
    for url in figures_df["Image URL"]:
        try:
    # Generate caption of image
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": url,
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            description = response.choices[0].message.content
        except Exception as e:
    #Error if necessary
            description = f"Error: {str(e)}"
    #Add captions to list
        descriptions.append(description)
    # Add captions to dataframe
    figures_df["Description"] = descriptions

    # Return dataframe containing the figure number, image key, image url, and figure description
    return figures_df

        

