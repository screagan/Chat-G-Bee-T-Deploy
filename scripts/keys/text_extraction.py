import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import extraction_functions 
from pypdf import PdfReader
import pandas as pd
import re

key_txt = "../../data/texts/bees-of-the-world-keys.pdf"
pdf = PdfReader(key_txt)


start_end = pd.read_csv("../../data/maps/section_start_end.csv", encoding = "cp1252", nrows=408)
additional = pd.read_csv("../../data/maps/start_end_extra.csv", index_col = 'index')
pages = pd.concat([start_end, additional])
num = pages['new_page'].tolist()


for i in range(len(pages)):
    t = extraction_functions.remove_before_after(pdf.pages[num[i] - 1].extract_text(), pages.loc[i]['start'], pages.loc[i]['end'])
    pages.loc[i, 'text'] = t

# pages = pd.read_csv('../../data/texts/bees-of-the-world-keys.csv', encoding = 'utf-8-sig').drop(columns=['index'])

sections = pages.groupby('section')['text'].apply(' '.join).reset_index()
sections['page_numbers'] = pages.groupby('section')['page'].apply(lambda x: list(x)).reset_index(drop = True)