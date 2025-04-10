from figures.hymenoptera.hymenopteraFigureDescriptions import generate_descriptions_of_hymenoptera_figures
from figures.MMD.MMDFigureDescriptions import generate_descriptions_of_MMD_figures
from text.chunkText import chunk_text_to_dataframe
from text.extractTextFromPDF import extract_text_from_pdf

mmd_text = extract_text_from_pdf(object_key="MMD-2022.pdf", bucket_name="ccber-tester-bucket")
mmd_text_chunks_df = chunk_text_to_dataframe(text=mmd_text, source="MMD")
print(mmd_text_chunks_df.head(10))
#Add hymenoptera to bucket once we know this works
# hymenoptera_text = extract_text_from_pdf(object_key="hymenoptera.pdf", bucket_name="ccber-tester-bucket")
# hymenoptera_text_chunks_df = chunk_text_to_dataframe()

mmd_figs_df = generate_descriptions_of_MMD_figures()
print(mmd_figs_df.head(10))

hymenoptera_figs_df = generate_descriptions_of_hymenoptera_figures()
print(hymenoptera_figs_df.head(10))

