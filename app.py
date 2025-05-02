import streamlit as st
import tempfile
import os
import fitz  # PyMuPDF
import easyocr
import json
from PIL import Image
import io
from format import format_ocr_data

st.set_page_config(page_title="PDF to Formatted JSON Converter", page_icon="📄")

def process_pdf(pdf_file):
    # Create a temporary directory to store the PDF
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded file to the temporary directory
        pdf_path = os.path.join(temp_dir, "uploaded.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])
        
        # Open the PDF with PyMuPDF
        doc = fitz.open(pdf_path)
        data = []
        
        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get the page as an image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Save the image temporarily
            img_path = os.path.join(temp_dir, f"page_{page_num}.png")
            img.save(img_path)
            
            # Perform OCR using EasyOCR
            result = reader.readtext(img_path)
            text = " ".join([item[1] for item in result])
            
            data.append({"page": page_num + 1, "text": text.strip()})
            
            # Clean up the temporary image
            os.remove(img_path)
        
        # Close the document
        doc.close()
        
        # Save OCR output
        ocr_output_path = os.path.join(temp_dir, "output_ocr.json")
        with open(ocr_output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Format the OCR data
        formatted_output_path = os.path.join(temp_dir, "formatted_output.json")
        format_ocr_data(ocr_output_path, formatted_output_path)
        
        # Read the formatted output
        with open(formatted_output_path, "r", encoding="utf-8") as f:
            formatted_data = json.load(f)
        
        return formatted_data

def main():
    st.title("📄 PDF to Formatted JSON Converter")
    st.write("Upload a PDF file to convert it into a formatted JSON file using OCR.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            try:
                # Process the PDF
                formatted_data = process_pdf(uploaded_file)
                
                # Display success message
                st.success("PDF processed successfully!")
                
                # Show preview of the formatted data
                st.subheader("Preview of Formatted Data")
                st.json(formatted_data)
                
                # Create download button
                json_str = json.dumps(formatted_data, indent=4, ensure_ascii=False)
                st.download_button(
                    label="Download Formatted JSON",
                    data=json_str,
                    file_name="formatted_output.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()