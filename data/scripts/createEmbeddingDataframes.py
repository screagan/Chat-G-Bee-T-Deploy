from figures.hymenoptera.hymenopteraFigureDescriptions import generate_descriptions_of_hymenoptera_figures
from figures.MMD.MMDFigureDescriptions import generate_descriptions_of_MMD_figures
from text.chunkText import chunk_text_to_dataframe
import pandas as pd

# First: Get text chunks from main text of MMD, put them into DF ready to be embedded
with open("data/MMD-Main-Text-Original.txt", "r", encoding="utf-8") as f:
     mmd_main_text = f.read()

mmd_text_chunks_df = chunk_text_to_dataframe(text=mmd_main_text, source_name="MMD")
mmd_text_chunks_df.to_csv("data/mmd_text_chunks.csv", index=False)
print(list(mmd_text_chunks_df.columns))

# Second: Get text chunks from main text of Hymenoptera once we have it, put them into DF ready to be embedded
# with open("data/Hymenoptera-Main-Text-Original.txt", "r", encoding="utf-8") as f:
#      hymenoptera_main_text = f.read()

# hymenoptera_text_chunks_df = chunk_text_to_dataframe(text=hymenoptera_main_text, source="Hymenoptera")
# print(hymenoptera_text_chunks_df.head(10))

# Third: Generate descriptions of MMD Figures, put them into DF ready to be embedded
mmd_figs_df = generate_descriptions_of_MMD_figures()
mmd_figs_df.to_csv("data/mmd_figs.csv", index=False)
print(list(mmd_figs_df.columns))

# Fourth: Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded
hymenoptera_figs_df = generate_descriptions_of_hymenoptera_figures()
hymenoptera_figs_df.to_csv("data/hymenoptera_figs.csv", index=False)
print(list(hymenoptera_figs_df.columns))

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat([mmd_text_chunks_df, mmd_figs_df, hymenoptera_figs_df], ignore_index=True)

# Save the combined DataFrame to a single CSV file
combined_df.to_csv("data/combined_data.csv", index=False)
print("Combined DataFrame saved to 'data/combined_data.csv'")