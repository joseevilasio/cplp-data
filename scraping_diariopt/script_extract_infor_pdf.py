from PyPDF2 import PdfReader


reader = PdfReader("scraping_diariopt/assets/raw_pdf/0004400044.pdf")
page = reader.pages[0]
print(page.extract_text())
