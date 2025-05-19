
from scripts.vectorstore.figures.getFiguresFromAWS import get_figures_from_AWS
import re
import pandas as pd

#This function outputs a dataframe consisting of figures, their s3 keys, their urls, and context (their references throughout the text)

def get_context_for_BOTW_figure_descriptions(main_text_chunks_df, keys_text_chunk_df):
    # Combined regex pattern to match figure references like "Fig. 7-5", "Figure 7-4", etc.
    figure_pattern = r'(?:Fig\.|Figure)\s+(\d+(?:-\d+)?)'
    
    data = []
    
    # Process main_text_chunks_df
    for _, row in main_text_chunks_df.iterrows():
        text = row['Text Content']
        if pd.isna(text):  # Skip if text is NaN
            continue
            
        matches = list(re.finditer(figure_pattern, text))
        for match in matches:
            figure_number = match.group(1)  # Extract just the figure number
            
            # Get context (the entire paragraph where figure is mentioned)
            context = text.strip()
            
            # Add metadata
            data.append({
                "Figure Number": figure_number,
                "Context": context,
                "Source": "main_text",
                "Title": row['Title'],
                "Page Number": row['Page Number'],
                "Author": row['Author']
            })
    
    # Process keys_text_chunk_df
    for _, row in keys_text_chunk_df.iterrows():
        text = row['Text Content']
        if pd.isna(text):  # Skip if text is NaN
            continue
            
        matches = list(re.finditer(figure_pattern, text))
        for match in matches:
            figure_number = match.group(1)  # Extract just the figure number
            
            # Get context (the entire paragraph where figure is mentioned)
            context = text.strip()
            
            # Add metadata
            data.append({
                "Figure Number": figure_number,
                "Context": context,
                "Source": "keys_text",
                "Title": row['Title'],
                "Page Number": row['Page Number'],
                "Author": row['Author']
            })
    
    # Convert to DataFrame
    if not data:  # Check if data list is empty
        return pd.DataFrame(columns=["Figure Number", "Context", "Source", "Title", "Page Number", "Author"])
    
    df_context = pd.DataFrame(data)
    
    # Group by 'Figure Number' and concatenate contexts
    df_context = df_context.groupby('Figure Number', as_index=False).agg({'Context': ' -- NEXT CONTEXT -- '.join})
    
    # Sort by figure number (handling compound numbers like "7-5")
    df_context['Sort Key'] = df_context['Figure Number'].apply(
        lambda x: [int(n) for n in x.split('-')]
    )
    df_context = df_context.sort_values(by='Sort Key')
    df_context = df_context.drop('Sort Key', axis=1)
    
    # Now, create DF with figure numbers, image keys and image urls from s3 bucket
    df_images = get_figures_from_AWS(
        bucket_name='ccber-tester-bucket', 
        aws_folder='BOTW-Figures/', 
        source_title='BOTW', 
        source_year='2007', 
        source_author='BOTWAuthor.', 
        source_publisher='BOTWPublisher'
    )
    
    # Merge the dataframes to match object urls with their corresponding context
    df_combined = pd.merge(df_images, df_context, on='Figure Number', how='inner')
    
    # Sort again by figure number for final output
    df_combined['Sort Key'] = df_combined['Figure Number'].apply(
        lambda x: [int(n) for n in x.split('-')]
    )
    df_combined = df_combined.sort_values(by='Sort Key')
    df_combined = df_combined.drop('Sort Key', axis=1)

    
    return df_combined