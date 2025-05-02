from pdf2image import convert_from_path
import pytesseract
import json

pdf_path = "GreenSapphire1_copy.pdf"
images = convert_from_path(pdf_path)
data = []

for i, img in enumerate(images):
    text = pytesseract.image_to_string(img)
    data.append({"page": i+1, "text": text.strip()})

with open("output_ocr.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
