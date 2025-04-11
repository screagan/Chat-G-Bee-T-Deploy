import re

#This function is used for texts like MMD, where references to the figure are spread throughout the source
# Standardizes figure references in a given text string.:
    # - Expands [Figs. 10-12] or Figs. 10-12 -> (Fig. 10) (Fig. 11) (Fig. 12)
    # - Converts [Figs. 4] or Figs 4 -> (Fig. 4)
    # - Converts [Figs. 469 and 470] or [Fig. 1 and 43] or Figs. 6,7 -> (Fig. 469) (Fig. 470) / (Fig. 1) (Fig. 43) / (Fig. 6) (Fig. 7)
    # - Converts Fig.1. -> (Fig. 1).
    # - Ensures consistent spacing
    # - Fixes missing closing brackets
    # - Prevents misinterpretation of `]` as `1`

def expand_figure_ranges(match):
    """ Expands figure ranges and formats them as individual (Fig. X) references. """
    start, end = int(match.group(1)), int(match.group(2))
    return " ".join(f"(Fig. {i})" for i in range(start, end + 1))

def expand_figure_list(match):
    """ Expands figure lists like 'Figs. 469 and 470' or 'Fig. 1 and 43' into separate (Fig. X) references. """
    numbers = re.split(r'\s*(?:and|,)\s*', match.group(1))
    return " ".join(f"(Fig. {num})" for num in numbers)

def standardize_figures(text):

    # Expand figure ranges, ensuring only three-digit numbers are matched
    text = re.sub(r'\(?Figs?\.?\s*(\d{1,3})\s*-\s*(\d{1,3})\)?', expand_figure_ranges, text)

    # Expand figure lists, ensuring numbers are properly formatted
    text = re.sub(r'\(?Figs?\.?\s*((?:\d{1,3}\s*(?:and|,)\s*)+\d{1,3})\)?', expand_figure_list, text)

    # Standardize individual figure references inside brackets (avoid double parentheses)
    text = re.sub(r'\(?Figs?\.?\s*(\d{1,3})\)?', r'(Fig. \1)', text)

    # Standardize inline figure references like "Fig.1." -> "(Fig. 1)."
    standardized_text = re.sub(r'(?<!\()Fig\.\s*(\d{1,3})(?!\))', r'(Fig. \1)', text)

    # Save to a file for manual editing. Pass in object_key as param to this function if you need it.
    # obj_key_without_file_type = object_key[:-4]
    with open(f"MMD-Keys-Text_standardized_text.txt", "w", encoding="utf-8") as f:
       f.write(text)

    return standardized_text