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

def standardize_MMD_figure_references(text):

    # Expand figure ranges, ensuring only three-digit numbers are matched
    text = re.sub(r'\(?Figs?\.?\s*(\d{1,3})\s*-\s*(\d{1,3})\)?', expand_figure_ranges, text)

    # Expand figure lists, ensuring numbers are properly formatted
    text = re.sub(r'\(?Figs?\.?\s*((?:\d{1,3}\s*(?:and|,)\s*)+\d{1,3})\)?', expand_figure_list, text)

    # Standardize individual figure references inside brackets (avoid double parentheses)
    text = re.sub(r'\(?Figs?\.?\s*(\d{1,3})\)?', r'(Fig. \1)', text)

    # Standardize inline figure references like "Fig.1." -> "(Fig. 1)."
    standardized_text = re.sub(r'(?<!\()Fig\.\s*(\d{1,3})(?!\))', r'(Fig. \1)', text)

    return standardized_text

if __name__ == "__main__":
    # Read in MMD text files, generated with standardizeMMDFigureReferences.py
    with open("data/texts/MMD-Main-Text.txt", "r", encoding="utf-8") as f:
        main_text = f.read()

    with open("data/texts/MMD-Keys.txt", "r", encoding="utf-8") as f:
        keys_text = f.read()

    # Standardize figure references in both texts
    standardized_main_text = standardize_MMD_figure_references(main_text)
    standardized_keys_text = standardize_MMD_figure_references(keys_text)

    # Save the standardized texts to new files
    with open("data/texts/MMD-Main-Text-With-Standardized-Fig-Refs.txt", "w", encoding="utf-8") as f:
        f.write(standardized_main_text)

    with open("data/texts/MMD-Keys-With-Standardized-Fig-Refs.txt", "w", encoding="utf-8") as f:
        f.write(standardized_keys_text)
    print("Standardized figure references and saved to new files.")