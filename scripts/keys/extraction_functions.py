from pypdf import PdfReader
import re
import pandas as pd
import fitz

#to be done: fix extract images function as they are returning in inverted colors, extract fig headings from descriptions

def remove_after_substr(text, substr):
    index = text.find(substr)
    if index != -1:
        return text[: index + len(substr)]
    return text

def remove_before_substr(text, substr):
    index = text.find(substr)
    if index != -1:
        return text[index :]
    return text

def  remove_before_after(text, b_str = None, a_str = None):
    t = text

    if b_str != None:
        b_index = t.find(b_str)
    else: 
        b_index = 0  

    if b_index != -1 and b_str != None:
        t = t[b_index :]

    if a_str != None:
        a_index = t.find(a_str)
    else: 
        a_index = len(t)  
    
    if a_index != -1 and a_str != None:
        t = t[: a_index + len(a_str)]
    
    return t

def trim_string(input_str, start_str, end_str):
    # Normalize the input, start, and end strings to handle any extra spaces
    start_str = re.sub(r'\s+', ' ', start_str.strip())  # Remove extra spaces in start_str
    end_str = re.sub(r'\s+', ' ', end_str.strip())      # Remove extra spaces in end_str

    # Create regex pattern for the start and end, allowing missing spaces
    start_pattern = re.escape(start_str).replace(" ", r"\s*")
    end_pattern = re.escape(end_str).replace(" ", r"\s*")

    # Find the starting index (start_str) with optional spaces around it
    start_index = re.search(r'\s*' + start_pattern + r'\s*', input_str)
    
    # If no start string match is found, return the original string up to the first part of the end pattern (if any)
    if not start_index:
        return input_str.strip()

    start_index = start_index.start()

    # Find the ending index (end_str) with optional spaces around it
    end_index = re.search(r'\s*' + end_pattern + r'\s*', input_str[start_index:])
    
    # If no end string match is found, return from start_str to the end of the original string
    if not end_index:
        return input_str[start_index:].strip()

    end_index = start_index + end_index.end()  # Adjust end_index relative to the original string

    # Return the substring between the start and end, trimming any surrounding spaces
    return input_str[start_index:end_index].strip()
    

def extract_keys(text):
    root = re.findall(r'(?m)(1\.)\s*(?s:(.*?))\.{3,}\s*([^\n]+)', text, flags = re.MULTILINE | re.DOTALL)

    if root != []:
        cleaned_root = [(root[0][0].strip(), root[0][1].strip(), root[0][2].strip(), '', '', '')]
        df_root = pd.DataFrame(cleaned_root, columns = ['id', 'left_text', 'left_target', 'sub_id', 'right_text', 'right_target'])
    else:
        df_root = pd.DataFrame()

    #pattern = r'^(?:(\d\(\d\)\.)\s*(?s:(.*?))(\.\.\. [^\n]*)|(—\.)\s*(?s:(.*?))(\.\.\. [^\n]*))'
    pattern = r'(?m)^(?:(\d+\(\d+\)\.)\s*(?s:(.*?))\s*\.\.\.\s*(.*?)(?=^\d+\(\d+\)\.|^—\.|\Z)|^(—\.)\s*(?s:(.*?))\s*\.\.\.\s*(.*?)(?=^\d+\(\d+\)\.|^—\.|\Z))'
    matches = re.findall(pattern, text, flags = re.MULTILINE | re.DOTALL)
        
    cleaned_matches = [(m[0].strip(), m[1].strip(), m[2].strip(), m[3].strip(), m[4].strip(), m[5].strip()) for m in matches]

    df_couplets = pd.DataFrame(cleaned_matches, columns = ['id', 'left_text', 'left_target', 'sub_id', 'right_text', 'right_target'])

    df = pd.concat([df_root, df_couplets]).reset_index(drop = True)

    return df

def clean_df(df, section_num, term = False):

    for i in range(len(df)):
        if df.loc[i, 'sub_id'] != '':
            df.loc[i-1, ['right_text', 'right_target']] = df.loc[i, ['right_text', 'right_target']]

    df = df[df['sub_id'] == ''].drop(columns = 'sub_id').reset_index(drop = True)

    for i in range(len(df)):
        if '(' in df.loc[i, 'id']:
            df.loc[i, 'parent'] = section_num + '-' + re.findall(r'\(([^)]*)\)', df.loc[i, 'id'])[0]

        if df.loc[i, 'id'] != '':
            df.loc[i, 'id'] = section_num + '-' + df.loc[i, 'id'][0]

        df.loc[i, 'left_text'] = re.sub(r'\.{2,}$', '.', df.loc[i, 'left_text']).replace('\n', ' ').replace('- ', '').replace('  ', ' ').replace(' .', '.')
        df.loc[i, 'left_target'] = re.sub(r'^[\s\.]+', '', df.loc[i, 'left_target']).replace('\n', ' ').strip()
        if df.loc[i, 'left_target'].isnumeric():
            df.loc[i, 'left_target'] = section_num + '-' + df.loc[i, 'left_target']
        df.loc[i, 'left_target_info'] = df.loc[i, 'left_target']

        df.loc[i, 'right_text'] = re.sub(r'\.{2,}$', '.', df.loc[i, 'right_text']).replace('\n', ' ').replace('- ', '').replace('  ', ' ').replace(' .', '.')
        df.loc[i, 'right_target'] = re.sub(r'^[\s\.]+', '', df.loc[i, 'right_target']).replace('\n', ' ').strip()
        if df.loc[i, 'right_target'].isnumeric():
            df.loc[i, 'right_target'] = section_num + '-' + df.loc[i, 'right_target'] 
        df.loc[i, 'right_target_info'] = df.loc[i, 'right_target']
        
        match = re.match(r'^(.*)\s+\(Sec\.\s*(\d+)\)$', df.loc[i, 'left_target'])
        if match:
            df.loc[i, 'left_target_info'] = match.group(1)
            df.loc[i, 'left_target'] = f'sec{match.group(2)}-1'
        else:
            df.loc[i, 'left_target_info'] = None

        match = re.match(r'^(.*)\s+\(Sec\.\s*(\d+)\)$', df.loc[i, 'right_target'])
        if match:
            df.loc[i, 'right_target_info'] = match.group(1)
            df.loc[i, 'right_target'] = f'sec{match.group(2)}-1'
        else:
            df.loc[i, 'right_target_info'] = None

        if term == True:
            df.loc[i, 'left_target_info'] = df.loc[i, 'left_target']
            df.loc[i, 'right_target_info'] = df.loc[i, 'right_target']

    return df

def create_terminal_points(df):
    terminal_points = pd.DataFrame(columns = ['id', 'description', 'parent'])
    for i in range(len(df)):
        if df.loc[i, 'left_target_info'] is not None:
            info = {
                'id' : df.loc[i, 'left_target'], 
                'description': df.loc[i, 'left_target_info'],
                'parent' : df.loc[i, 'id']
            }

            terminal_points = pd.concat([terminal_points, pd.DataFrame(info, index = [0])])

        if df.loc[i, 'right_target_info'] is not None:
            info = {
                'id' : df.loc[i, 'right_target'], 
                'description': df.loc[i, 'right_target_info'],
                'parent' : df.loc[i, 'id']
            }

            terminal_points = pd.concat([terminal_points, pd.DataFrame(info, index = [0])]).reset_index(drop = True)

    return terminal_points

def extract_images(pdf_path, page_numbers, output_dir="../../data/imgs"):
    pdf_document = fitz.open(pdf_path)

    for page_num in page_numbers:
        if 1 <= page_num <= len(pdf_document):
            page = pdf_document[page_num - 1]  # Access page with 0-based indexing
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_filename = f"page_{page_num}_img_{img_index + 1}.{image_ext}"
                image_path = f"{output_dir}/{image_filename}"

                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                print(f"Image saved: {image_path}")
        else:
            print(f"Page number {page_num} is out of range for the PDF.")