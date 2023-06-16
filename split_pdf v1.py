import os
import shutil
import tkinter as tk
from tkinter import filedialog
import pdfplumber
import PyPDF2
import re

def extract_name_from_pension_statement(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        # Search for the name pattern using regular expression
        name_pattern = r"(?i)NAME OF MEMBER[\s:]+(.+)"
        match = re.search(name_pattern, text)

        if match:
            # Extract the full name from the match
            extracted_name = match.group(1).strip()
            return extracted_name

        return None

def split_pdf():
    # Prompt the user to select the input PDF file
    tk.Tk().withdraw()
    input_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not input_path:
        print("No input file selected.")
        return
    
    # Prompt the user to select the output directory
    tk.Tk().withdraw()
    output_dir = filedialog.askdirectory()
    if not output_dir:
        print("No output directory selected.")
        return

    # Prompt the user for the renaming option
    rename_option = input("Do you want to extract the name from the pension statement and rename the PDF files? (Y/N): ")
    rename_option = rename_option.upper()

    # Open the PDF file
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

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

            if rename_option == 'Y':
                extracted_name = extract_name_from_pension_statement(output_path)
                if extracted_name:
                    # Create the new file name
                    new_filename = extracted_name + '.pdf'
                    new_path = os.path.join(output_dir, new_filename)

                    try:
                        os.rename(output_path, new_path)
                        print(f"Renamed file '{file_name}' to '{new_filename}'")
                    except FileNotFoundError:
                        print(f"File '{file_name}' not found. Skipping renaming.")
                    except Exception as e:
                        print(f"Error occurred while renaming '{file_name}': {str(e)}")
                else:
                    print(f"Name pattern not found in '{file_name}'. Skipping renaming.")

        print("PDF splitting and renaming completed.")

# Run the function to split the PDF file
split_pdf()
