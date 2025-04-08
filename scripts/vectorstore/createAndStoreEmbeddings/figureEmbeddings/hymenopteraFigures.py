# First, we need to generate captions for our figures in the hymenoptera data source.
# This works well for figures which have a caption within view of the figure.

import boto3
from openai import OpenAI

# Function to list all object URLs in the bucket
def list_s3_object_urls(bucket_name, s3_client):
    object_urls = []
    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if "Contents" in response:
        for obj in response["Contents"]:
            object_key = obj["Key"]
            object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
            object_urls.append(object_url) #TODO: ADD FILTERING SO IT ONLY GRABS HYMENOPTERA FIGURES
    print("\nList of Object URLs:")
    for url in object_urls:
        print(url)
    return object_urls


def generate_descriptions_of_hymenoptera_figures(openai_api_key, aws_access_key_id, aws_secret_access_key, bucket_name):

    s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
    )

    openai_client = OpenAI(api_key=openai_api_key)

    object_urls = list_s3_object_urls(bucket_name, s3_client) 

    for url in object_urls:
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

        print(f"\n🔗 Image URL: {url}\n📝 Caption: {caption}\n" + "-"*80)

