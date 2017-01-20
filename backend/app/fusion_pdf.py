import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileMerger

files_dir = "C:\\olatest\\app\\pdf"
pdf_files = [f for f in os.listdir(files_dir) if f.endswith("pdf")]
merger = PdfFileMerger()

for filename in pdf_files:
    merger.append(PdfFileReader(os.path.join(files_dir, filename), "rb"))

merger.write(os.path.join(files_dir, "merged_full.pdf"))
