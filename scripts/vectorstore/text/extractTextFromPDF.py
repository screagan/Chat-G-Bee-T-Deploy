import boto3
import pdf2image
import pytesseract
from scripts.utils.client_provider import ClientProvider

def extract_text_from_pdf(object_key, bucket_name, num_columns, crop_top_pixels=150):
    """
    Extracts text from a PDF stored in an S3 bucket.

    Parameters:
        object_key (str): The key for the PDF file in S3.
        bucket_name (str): The name of the S3 bucket.
        num_columns (int): Number of text columns per page (1 or 2).
        crop_top_pixels (int): Number of pixels to crop from the top of each page image. Helpful if unwanted page headers.

    Returns:
        List of dicts with keys 'text' and 'page_num'.
    """
    s3 = ClientProvider.get_s3_client()
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    pdf_bytes = response["Body"].read()
    images = pdf2image.convert_from_bytes(pdf_bytes)
    extracted_texts = []

    for page_num, image in enumerate(images, 1):
        width, height = image.size

        # Crop top section if specified
        if crop_top_pixels > 0:
            image = image.crop((0, crop_top_pixels, width, height))
            height -= crop_top_pixels  # Update height

        if num_columns == 1:
            text = pytesseract.image_to_string(image, config='--psm 6')
            extracted_texts.append({
                'text': text,
                'page_num': page_num
            })
            print(f"Extracted text from page {page_num} (single-column) of {object_key}")

        elif num_columns == 2:
            midpoint = width // 2
            left_column = image.crop((0, 0, midpoint, height))
            right_column = image.crop((midpoint, 0, width, height))

            left_text = pytesseract.image_to_string(left_column, config='--psm 6')
            right_text = pytesseract.image_to_string(right_column, config='--psm 6')

            full_text = left_text + '\n' + right_text
            print(full_text)
            extracted_texts.append({
                'text': full_text,
                'page_num': page_num
            })
            print(f"Extracted text from page {page_num} (two-column) of {object_key}")

        else:
            raise ValueError("Only num_columns=1 or 2 are supported.")

    return extracted_texts
