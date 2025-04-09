
from scripts.vectorstore.createAndStoreEmbeddings.figures.getFiguresFromAWS import get_figures_from_source
import re
import pandas as pd

#This function outputs a dataframe consisting of figures, their s3 keys, their urls, and context (their references throughout the text)
#The MMD source is split into two objects in our s3 Bucket, so we will reference them seperately here
def get_context_for_MMD_figure_descriptions(main_text, keys_text, context_size=100, skip_forward=50):

    """
    Extracts mentions of figures in the format (Fig. X) from text using regex and returns a DataFrame.

    Args:
    - keys_text (str): The long text from the keys section of the pdf.
    - main_text (str): The long text from the main text section of the pdf.
    - context_size (int): Number of characters to include as context before and after the match.
    - skip_forward (int): Number of characters to skip after finding a match to avoid overlapping contexts.

    Returns:
    - DataFrame with 'Figure Number' and 'Context'.
    """

    # Regex pattern to match ONLY (Fig. X)
    figure_pattern = r'\(Fig\. \d+\)'

    main_text_matches = list(re.finditer(figure_pattern, main_text))

    data = []

    last_main_text_index = 0  # Track the last processed position within main text
    for match in main_text_matches:
        start, end = match.start(), match.end()

        # Ensure we don't extract overlapping contexts
        if start < last_main_text_index:
            continue  # Skip if within the skip range of the last match

        figure_number = match.group(0)  # Extract matched (Fig. X)

        # Extract context
        context = main_text[max(0, start - context_size): min(len(main_text), end + context_size)]

        # Extract just the number, to feed to DF. TODO: Change by using Apply function maybe, like do this line below later to all at once. Think through tho
        figure = int(re.search(r'\d+', figure_number).group())
        data.append({"Figure": figure, "Context": context})

        # Update last_index to enforce skip
        last_index = end + skip_forward

    keys_text_matches = list(re.finditer(figure_pattern, keys_text))
    last_keys_text_index = 0 # Track the last processed position within key text
    for match in keys_text_matches:
        start, end = match.start(), match.end()

        # Ensure we don't extract overlapping contexts
        if start < last_keys_text_index:
            continue  # Skip if within the skip range of the last match

        figure_number = match.group(0)  # Extract matched (Fig. X)
        figure = int(re.search(r'\d+', figure_number).group())

        # Search backwards for a stopping point
        prev_section_match = re.search(r'\);\s|\];\s', keys_text[:start][::-1])  # Find the previous `);` or `];`
        prev_figure_match = re.search(figure_pattern, keys_text[:start][::-1])  # Find the previous figure mention

        # Determine the closest stopping point
        if prev_section_match:
            stop_index = start - prev_section_match.start()
        elif prev_figure_match:
            stop_index = start - prev_figure_match.start()
        else:
            stop_index = max(0, start - 100)  # Default max of 100 chars if neither is found

        # Ensure we don't start at an incomplete word
        #stop_index = max(0, stop_index)

        context = keys_text[stop_index:end]

        data.append({"Figure": figure, "Context": context})

        # Update last index to enforce skip
        last_keys_text_index = end + skip_forward


    # Convert to DataFrame
    df_context = pd.DataFrame(data)

    # Group by 'Figure Number' and concatenate contexts
    df_context = df_context.groupby('Figure', as_index=False).agg({'Context': ' -- NEXT CONTEXT -- '.join})

    # Sort by extracted numeric figure, we do this again later so we dont have to now, but it's nicer on the eys
    df_context['Figure'] = df_context['Figure']
    df_context = df_context.sort_values(by='Figure')


    #Now, create DF with figure numbers, image keys and image urls from s3 bucket (TODO: Unhardcode this)
    df_images = get_figures_from_source(bucket_name = 'ccbeer-tester-bucket', source_name = 'MMD-Figures/')

    #Now, merge the dataframes to match object urls with their corresponding context
    df_combined = pd.merge(df_images, df_context, on='Figure', how='inner')
    df_combined = df_combined.sort_values(by='Figure')

    return df_combined

