import os
import PyPDF2
import pdfplumber

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text = text + " " + page.extract_text()
        return text
        
#text_bees = extract_text("../data/bees-of-the-world.pdf")
#with open("../data/bees-of-the-world.txt", "w", encoding = "utf-8") as file:
#    file.write(text_bees)

# text_hymenoptra = extract_text("../data/hymenoptera-of-the-world.pdf")
# with open("../data/hymenoptra-of-the-world.txt", "w", encoding = "utf-8") as file:
#     file.write(text_hymenoptra)

# text_mmd = extract_text("../data/mmd-2022.pdf")
# with open("../data/mmd-2022.txt", "w", encoding = "utf-8") as file:
#     file.write(text_mmd)

# text = text_bees + " " + text_hymenoptra + " " + text_mmd
# with open("../data/text-combined.txt", "w", encoding = "utf-8") as file:
#     file.write(text)