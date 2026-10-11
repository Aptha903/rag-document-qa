from pathlib import Path
from pypdf import PdfReader

for pdf in sorted(Path("docs").glob("*.pdf")):
    reader = PdfReader(pdf)
    text = reader.pages[0].extract_text()
    print(pdf.name, "|", len(reader.pages), "pages |", len(text), "chars on page 1")