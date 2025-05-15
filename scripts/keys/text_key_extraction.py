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

pages = pd.read_csv('../../data/texts/bees-of-the-world-keys.csv', encoding = 'utf-8-sig').drop(columns=['index'])

raw_keys = pd.read_csv("../../data/keys/bees-of-the-world-tree-texts.csv", encoding = 'utf-8-sig').drop(columns = ['id'])

raw_keys['subsection_num'] = raw_keys.groupby('section_num').cumcount() + 1
raw_keys['id'] = "sec" + raw_keys['section_num'].astype(str) + "-" + raw_keys['subsection_num'].astype(str)
raw_keys = raw_keys.drop(columns = ['section_num', 'subsection_num'])

def extract_title(text):
    match = re.search(r'^(.*?)\n1\.', text, re.DOTALL)
    if match:
        return match.group(1).strip().replace('\n', '')
    else:
        return None

raw_keys['title'] = raw_keys['text'].astype(str).apply(extract_title)
raw_keys['tree_level'] = raw_keys['tree_level'].str.rstrip('s').str.lower()
raw_keys = raw_keys.map(lambda x: x.replace('T ribe', "Tribe") if isinstance(x, str) else x)

#raw_keys.to_csv('../../data/keys/raw_key_index.csv', index = False, encoding = 'utf-8-sig')

for i in range(len(raw_keys)):
    if raw_keys.loc[i, 'tree_level'] in ['family', 'subfamily', 'tribe']:
        nodes = extraction_functions.clean_df(extraction_functions.extract_keys(raw_keys['text'][i]), raw_keys['id'][i])
        terminal_nodes = extraction_functions.create_terminal_points(nodes)

    elif raw_keys.loc[i, 'tree_level'] in ['genera', 'subgenera', 'group']:
        nodes = extraction_functions.clean_df_mod(extraction_functions.extract_keys(raw_keys['text'][i]), raw_keys['id'][i])
        terminal_nodes = extraction_functions.create_terminal_points(nodes)

    #nodes.to_csv(f"../../data/keys/nodes/{raw_keys['id'][i]}-nodes.csv", encoding = 'utf-8-sig', index = False)
    #terminal_nodes.to_csv(f"../../data/keys/terminal-nodes/{raw_keys['id'][i]}-terminalnodes.csv", encoding = 'utf-8-sig', index = False)

def split_on(text):
    if "of the" in text:
        return text.split("of the", 1)
    elif "of" in text:
        return text.split("of", 1)
    else:
        return [text]
    
def insert_after_word(original_string, word, string_to_insert):
    index = original_string.find(word)
    if index == -1:
        return original_string
    else:
        return original_string[:index + len(word)] + string_to_insert + original_string[index + len(word):]
    
def reformat_genera_title(title, term_node, tree_level):
    if "Key" in title:
        new_title = title.replace("Key", "Characteristics")
    elif "Keys" in title:
        new_title = title.replace("Keys", "Characteristics")
    
    if tree_level == 'genera':
        new_title = insert_after_word(new_title, "Genera", " " + term_node)
    elif tree_level == 'subgenera':
        new_title = insert_after_word(new_title, "Subgenera", " " + term_node)
    elif tree_level == 'group':
        new_title = insert_after_word(new_title, "Groups", " " + term_node)

    return new_title

def get_description(term_node):
    row = df_terminal[df_terminal['description'] == term_node]
    if row.empty:
        return None
    
    node_id = row.iloc[0]['id']
    path = []

    while node_id in parent_map:
        parent_id, decision_text = parent_map[node_id]
        if decision_text:
            path.append(f"- {decision_text.strip()}")
        node_id = parent_id

    return "\n".join(reversed(path))

def create_description(term_node):
    sec = os.path.basename(node_path).replace("-nodes.csv", "")
    if raw_keys.loc[raw_keys['id'] == sec, 'tree_level'].iloc[0] == 'family':
        desc = f"Characteristics of the Family {term_node}," + raw_keys.loc[raw_keys['id'] == sec, 'title'].iloc[0].split(',')[1] + ":\n"
    
    elif raw_keys.loc[raw_keys['id'] == sec, 'tree_level'].iloc[0] == 'subfamily':
        desc = f"Characteristics of the Subfamily {term_node}," + " of the" + split_on(raw_keys.loc[raw_keys['id'] == sec, 'title'].iloc[0])[1] + ":\n"

    elif raw_keys.loc[raw_keys['id'] == sec, 'tree_level'].iloc[0] == 'tribe':
        desc = f"Characteristics of the Tribe {term_node}," + " of the" + split_on(raw_keys.loc[raw_keys['id'] == sec, 'title'].iloc[0])[1] + ":\n"
    elif raw_keys.loc[raw_keys['id'] == sec, 'tree_level'].iloc[0] in ['genera', 'subgenera', 'group']:
        desc = reformat_genera_title(raw_keys.loc[raw_keys['id'] == sec, 'title'].iloc[0], term_node, raw_keys.loc[raw_keys['id'] == sec, 'tree_level'].iloc[0]) + ":\n"
    return desc

full_term_nodes = pd.DataFrame(columns = ['id', 'description', 'parent'])

for i in range(len(raw_keys)):
    current_path = f"../../data/keys/terminal-nodes/{raw_keys['id'][i]}-terminalnodes.csv"
    current = pd.read_csv(current_path, encoding = 'utf-8-sig')
    current['tree_id'] = raw_keys['id'][i]
    full_term_nodes = pd.concat([full_term_nodes, current], ignore_index = True)

#full_term_nodes.dropna().to_csv("../../data/keys/full_terminal_nodes.csv", index = False, encoding = 'utf-8-sig')

full_term_nodes = pd.read_csv("../../data/keys/full_terminal_nodes.csv", encoding = 'utf-8-sig')

for i in range(len(full_term_nodes)):
    node_path = f"../../data/keys/nodes/{full_term_nodes.loc[i, 'tree_id']}-nodes.csv"
    term_path = f"../../data/keys/terminal-nodes/{full_term_nodes.loc[i, 'tree_id']}-terminalnodes.csv"

    df_nodes = pd.read_csv(node_path)
    df_terminal = pd.read_csv(term_path)

    parent_map = {}

    for _, row in df_nodes.iterrows():
        if pd.notna(row['left_target']):
            parent_map[row['left_target']] = (row['id'], row['left_text'])
        if pd.notna(row['right_target']):
            parent_map[row['right_target']] = (row['id'], row['right_text'])

    for _, row in df_terminal.iterrows():
        if row['id'] not in parent_map:
            parent_map[row['id']] = (row['parent'], None)

    x = create_description(full_term_nodes.loc[i, 'description'])
    y = get_description(full_term_nodes.loc[i, 'description'])
    
    full_term_nodes.loc[i, 'characteristics'] = x + y

#full_term_nodes.to_csv("../../data/keys/full_descriptions.csv", index = False, encoding = 'utf-8-sig')

desc = pd.read_csv("../../data/keys/full_descriptions.csv", encoding = 'utf-8-sig')

#with open("../../data/texts/bees-of-the-world-key-descriptions.txt", "a", encoding = 'utf-8-sig') as file:
#    for i in range(len(desc)):
#        file.write("=====\n")
#        file.write(desc['characteristics'][i])
#        file.write("\n")