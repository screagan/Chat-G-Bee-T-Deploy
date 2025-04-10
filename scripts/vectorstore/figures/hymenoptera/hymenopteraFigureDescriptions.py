from openai import OpenAI
from ..getFiguresFromAWS import get_figures_from_source
from dotenv import load_dotenv
import os


# We need to generate captions for our figures in the hymenoptera data source.
# This works well for figures which have a caption within view of the figure.

def generate_descriptions_of_hymenoptera_figures(): #TODO: Check this source_name in s3 bucket

    #get openai api key and create client
    load_dotenv()
    openai_api_key = os.getenv("API_KEY")
    openai_client = OpenAI(api_key=openai_api_key)
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    #Get dataframe containing figures from hymenoptera
    figures_df = get_figures_from_source(bucket_name=bucket_name, source_name='Hymenoptera-Figures/') 
    print(type(figures_df))
    captions = []
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
            caption = response.choices[0].message.content
        except Exception as e:
    #Error if necessary
            caption = f"Error: {str(e)}"
        print(f"\n🔗 Image URL: {url}\n📝 Caption: {caption}\n" + "-"*80)
    #Add captions to list
        captions.append(caption)
    # Add captions to dataframe
    figures_df["Caption"] = captions

    # Return dataframe containing the figure number, image key, image url, and figure description
    return figures_df

        

