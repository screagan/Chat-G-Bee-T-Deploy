from figures.hymenoptera.hymenopteraFigureDescriptions import generate_descriptions_of_hymenoptera_figures
from figures.MMD.MMDFigureDescriptions import generate_descriptions_of_MMD_figures
from text.chunkText import chunk_text_to_dataframe


# First: Get text chunks from main text of MMD, put them into DF ready to be embedded
with open("data/MMD-Main-Text-Original.txt", "r", encoding="utf-8") as f:
     mmd_main_text = f.read()

mmd_text_chunks_df = chunk_text_to_dataframe(text=mmd_main_text, source="MMD")
print(mmd_text_chunks_df.head(10))

# Second: Get text chunks from main text of Hymenoptera once we have it, put them into DF ready to be embedded
# with open("data/Hymenoptera-Main-Text-Original.txt", "r", encoding="utf-8") as f:
#      hymenoptera_main_text = f.read()

# hymenoptera_text_chunks_df = chunk_text_to_dataframe(text=hymenoptera_main_text, source="Hymenoptera")
# print(hymenoptera_text_chunks_df.head(10))

# Third: Generate descriptions of MMD Figures, put them into DF ready to be embedded
mmd_figs_df = generate_descriptions_of_MMD_figures()
print(mmd_figs_df.head(10))

# Fourth: Generate descriptions of Hymenoptera Figures, put them into DF ready to be embedded
hymenoptera_figs_df = generate_descriptions_of_hymenoptera_figures()
print(hymenoptera_figs_df.head(10))

