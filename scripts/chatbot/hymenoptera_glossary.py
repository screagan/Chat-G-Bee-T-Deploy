import re

def extract_glossary_terms(response, glossary):
    found_terms = []
    response_lower = response.lower()
    
    for term in glossary:
        # Escape special regex characters in term
        escaped_term = re.escape(term.lower())
        
        # Pattern allows optional 's' for plural
        pattern = r'\b' + escaped_term + r's?\b'
        
        if re.search(pattern, response_lower):
            found_terms.append(term)
            
    return found_terms

def extract_terms_and_definitions(text):
    lines = text.splitlines()
    glossary = {}
    current_term = None
    current_def = []

    term_pattern = re.compile(
        r"^([a-z][a-z \-]+)\s+((?:\([^)]+\)\s+)?[A-Z].+)"
    )

    for line in lines:
        line = line.strip()

        if not line:
            continue

        match = term_pattern.match(line)
        if match:
            # Save previous term
            if current_term:
                glossary[current_term] = " ".join(current_def).strip()

            # Start new term
            current_term = match.group(1).strip()
            current_def = [match.group(2).strip()]
        else:
            if current_term:
                current_def.append(line)

    # Add the last captured term
    if current_term:
        glossary[current_term] = " ".join(current_def).strip()

    return glossary

    
with open("data/texts/hymenoptera_of_the_world_keywords.txt", "r", encoding="utf-8") as f:
    full_text = f.read()


GLOSSARY = extract_terms_and_definitions(full_text)

# Need to fix one keyword
# 1. Extract and fix the original value
original_1 = GLOSSARY['mesotrochantinal plate']
fixed_1, new_def_1 = original_1.split("met-, meta-", 1)

original_2 = GLOSSARY['malar space']
fixed_2, new_def_2 = original_2.split("mes-, meso-", 1)

# 2. Update the existing definition
GLOSSARY['mesotrochantinal plate'] = fixed_1.strip()
GLOSSARY['malar space'] = fixed_2.strip()

# 3. Add the new correct key
GLOSSARY['met-, meta-'] = "A Greek prefix meaning hind or posterior; used with Latin, latinized, or Greek words to indicate the posterior (usually third) part of a structure."
GLOSSARY['mes- meso-'] = "A Greek prefix meaning middle or mid; used with Latin, latinized, or Greek words to indicate the middle (often second) part of a structure."

print(len(GLOSSARY))