import re
import pandas as pd
from scripts.utils.client_provider import ClientProvider
# Takes in a bucket name and source name, outputs a dataframe containing the figures, their s3 keys and their urls.

def get_figures_from_AWS(bucket_name, aws_folder, source_title, source_year, source_author, source_publisher):
  s3 = ClientProvider.get_s3_client()
  s3_objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=aws_folder)
  
  # Prepare to get metadata
  figure_numbers = []
  page_numbers = []
  image_keys = []
  image_urls = []
  
  # Check if the bucket is empty
  if 'Contents' not in s3_objects:
    print(f"No objects found in bucket '{bucket_name}' with prefix '{aws_folder}', please check your s3 bucket and make sure folder exists.")
    return 
  
  for obj in s3_objects['Contents']:
    print(obj["Key"])
    file_type = obj["Key"][-3:]
    img_key = obj["Key"]

    if file_type == 'png' or file_type == 'jpg' or file_type == 'peg': #Make sure object is an image
      # Enhanced pattern to match both simple and compound figure numbers
      figure_match = re.search(r'img_(\d+(?:-\d+)?)', img_key)
      if figure_match:
        figure_number = figure_match.group(1)
        # Check if this is a compound figure number
        if '-' in figure_number:
          # For compound figures like "7-5", keep as string
          pass
        else:
          # For simple figures like "7", convert to int for backward compatibility
          figure_number = int(figure_number)
      else:
        print(f"Could not extract figure number from {img_key}")
        continue
      
      # Extract page number
      match = re.search(r'(?:page_|pg_)(\d+)_img', img_key)
      if match:
        page_numbers.append(int(match.group(1)))
      else:
        page_numbers.append('NA')
      
      # Create URL
      img_url = f'https://{bucket_name}.s3.us-east-1.amazonaws.com/{img_key}'

      # Append to lists
      figure_numbers.append(figure_number)
      image_keys.append(img_key)
      image_urls.append(img_url)

    else:
      print(f'File type {file_type} not supported. Skipping {img_key}')
      continue

  data = {
      'Title': source_title,
      'Year': source_year,
      'Author': source_author,
      'Publisher': source_publisher,
      'Page Number': page_numbers,
      'Type': 'Image',
      'Text Content': 'NA',
      'Figure Number': figure_numbers,
      'Image Key': image_keys,
      'Image URL': image_urls,
  }
  
  df = pd.DataFrame(data)
  return df
