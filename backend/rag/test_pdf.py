from pypdf import PdfReader

reader = PdfReader("data/books/MakerIKSbook1.docx.pdf")

text = reader.pages[0].extract_text()

print(repr(text[:1000]))