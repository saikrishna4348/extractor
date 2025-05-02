import streamlit as st
import tempfile
import os
from pdf2image import convert_from_path
import pytesseract
import json
from format import format_ocr_data

st.set_page_config(page_title="PDF to Formatted JSON Converter", page_icon="📄")

def process_pdf(pdf_file):
    # Create a temporary directory to store the PDF
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded file to the temporary directory
        pdf_path = os.path.join(temp_dir, "uploaded.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        data = []
        
        # Process each page with OCR
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            data.append({"page": i+1, "text": text.strip()})
        
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
                  # Create download button
                json_str = json.dumps(formatted_data, indent=4, ensure_ascii=False)
                st.download_button(
                    label="Download Formatted JSON",
                    data=json_str,
                    file_name="formatted_output.json",
                    mime="application/json"
                )
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