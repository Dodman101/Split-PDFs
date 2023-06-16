import os
import PyPDF2
from tkinter import Tk
from tkinter import filedialog

def split_pdf():
    # Prompt the user to select the input PDF file
    Tk().withdraw()
    input_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not input_path:
        print("No input file selected.")
        return
    
    # Prompt the user to select the output directory
    Tk().withdraw()
    output_dir = filedialog.askdirectory()
    if not output_dir:
        print("No output directory selected.")
        return

    # Open the PDF file
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Iterate over each page
        for page_num in range(len(pdf_reader.pages)):
            # Create a new PDF writer
            pdf_writer = PyPDF2.PdfWriter()
            
            # Add the current page to the writer
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Create the output file path
            file_name = f'page_{page_num + 1}.pdf'
            output_path = os.path.join(output_dir, file_name)
            
            # Write the output PDF file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                
            print(f'Split page {page_num + 1} saved as {file_name}')

# Run the function to split the PDF file
split_pdf()