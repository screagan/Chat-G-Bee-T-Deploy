import boto3
import pdf2image
import pytesseract
from utils.client_provider import ClientProvider

# Gets PDF from AWS s3 Bucket and extracts text, returning a string

def extract_text_from_pdf(object_key, bucket_name): 
    # Load environment variables from the .env file
    s3 = ClientProvider.get_s3_client()

    # Download the PDF file into memory
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    pdf_bytes = response["Body"].read()

    # Convert PDF pages to images
    images = pdf2image.convert_from_bytes(pdf_bytes)

    # Extract text using Tesseract OCR
    extracted_texts = []
    for page_num, image in enumerate(images, 1):  # Start page numbering from 1
        text = pytesseract.image_to_string(image, config='--psm 6')
        # Store both text and page number
        extracted_texts.append({
            'text': text,
            'page_num': page_num  #TODO: Realize that we may not want to start on page 1, for example if in AWS the whole textbook is not there
        })
        print(f"Extracted text from page {page_num} of {object_key}")

    # For the text file output (keep the combined version for file writing)
    # combined_text = "\n".join([item['text'] for item in extracted_texts]).strip()
    # obj_key_without_file_type = object_key[:-4]
    # with open(f"{obj_key_without_file_type}_extracted_text.txt", "w", encoding="utf-8") as f:
    #     f.write(combined_text)
    
    return extracted_texts  # Return the list of dicts with text and page numbers