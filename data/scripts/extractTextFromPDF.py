import boto3
import pdf2image
import pytesseract
from scripts.utils.client_provider import ClientProvider

# Gets PDF from AWS s3 Bucket and extracts text, returning a string

def extract_text_from_pdf(object_key, bucket_name) -> str:
    # Load environment variables from the .env file
    s3 = ClientProvider.get_s3_client()

    # Download the PDF file into memory
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    pdf_bytes = response["Body"].read()

    # Convert PDF pages to images
    images = pdf2image.convert_from_bytes(pdf_bytes)

    # Extract text using Tesseract OCR
    extracted_text = []
    for page_num, image in enumerate(images):  # Adjust page range here if needed
        text = pytesseract.image_to_string(image, config='--psm 6')  # Use PSM mode 6 (assumes structured text)
        extracted_text.append(text)
        print(f"Extracted text from page {page_num} of {object_key}")

    extracted_text = "\n".join(extracted_text).strip()
    # To write text to text file, which we probably want to do later:
    obj_key_without_file_type = object_key[:-4]
    with open(f"{obj_key_without_file_type}_extracted_text.txt", "w", encoding="utf-8") as f:
       f.write(extracted_text)
    return extracted_text