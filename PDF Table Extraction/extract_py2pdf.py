import PyPDF2

text = ""

with open('documents/safari.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        
        page_text = page.extract_text()
        
        text += page_text + "\n\n"
        
    return text
        
