# PDF to Formatted JSON Converter

A Streamlit application that converts PDF files into formatted JSON using OCR (Optical Character Recognition) with optional handwriting detection.

## Features

- Upload PDF files through a user-friendly interface
- Automatic OCR processing of PDF content
- Optional handwriting detection mode
- Image preprocessing for better text recognition
- Preview of the formatted JSON output
- Download the formatted JSON file
- Clean and modern UI

## Prerequisites

Before running the application, you need to install:

1. Python 3.7 or higher
2. Tesseract OCR engine
3. Poppler (for PDF processing)
4. OpenCV (for image preprocessing)

### Installing Tesseract OCR

#### Windows
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Add Tesseract to your system PATH
4. Download the handwriting model from: https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata
5. Place the handwriting model in your Tesseract tessdata directory

#### Linux
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng
```

#### macOS
```bash
brew install tesseract
brew install tesseract-lang
```

### Installing Poppler

#### Windows
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Add the bin directory to your system PATH

#### Linux
```bash
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install poppler
```

## Installation

1. Clone this repository
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)
3. Choose whether to enable handwriting detection (checkbox)
4. Upload a PDF file using the file uploader
5. Wait for the processing to complete
6. Preview the formatted JSON output
7. Download the formatted JSON file using the download button

## Notes

- The application processes PDFs page by page
- OCR quality depends on the PDF quality and text clarity
- Handwriting detection may be slower than regular text detection
- Image preprocessing is applied to improve recognition accuracy
- Large PDFs may take longer to process
- For best results with handwriting:
  - Use clear, well-lit scans
  - Ensure consistent handwriting
  - Avoid overlapping text
  - Use good quality paper with minimal background noise 