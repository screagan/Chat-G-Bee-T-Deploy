from utils.client_provider import ClientProvider
from ..getFiguresFromAWS import get_figures_from_AWS
import os

# We need to generate captions for our figures in the hymenoptera data source.
# This works well for figures which have a caption within view of the figure.

def generate_descriptions_of_HOTW_figures():

    # Create OpenAI Client
    openai_client = ClientProvider.get_openai_client()

    #Get dataframe containing figures from hymenoptera
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    figures_df = get_figures_from_AWS(bucket_name=bucket_name, aws_folder='HOTW-Figures/', source_title="Hymenoptera of the World", source_year='1993', source_author='John I Huber', source_publisher='HOTWPublisher') 
    
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
        print("Created description for image:", url)
        descriptions.append(description)
    # Add captions to dataframe
    figures_df["Image Description"] = descriptions

    # Return dataframe containing the figure number, image key, image url, and figure description
    return figures_df

        

