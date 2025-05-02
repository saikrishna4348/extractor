import re
import json
import os

def format_ocr_data(input_file="output_ocr.json", output_file="formatted_output.json"):
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} not found")

        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        formatted = []
        
        # Handle both single page and multi-page formats
        if isinstance(data, list):
            pages = data
        else:
            pages = [data]

        for page in pages:
            page_dict = {}
            # Handle different possible structures
            if 'text' in page:
                text = page['text']
            elif 'content' in page:
                text = page['content']
            else:
                text = str(page)

            # Split into lines and process
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Try to match key: value pattern
                match = re.match(r"(.+?):\s*(.+)", line)
                if match:
                    key, value = match.groups()
                    page_dict[key.strip()] = value.strip()
                else:
                    # If no key:value pattern, store the whole line
                    page_dict[f"line_{len(page_dict) + 1}"] = line

            # Add page number if available
            page_num = page.get('page', len(formatted) + 1)
            formatted.append({f"page_{page_num}": page_dict})

        # Save formatted output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted, f, indent=4, ensure_ascii=False)
        
        print(f"Successfully formatted data and saved to {output_file}")
        return True

    except json.JSONDecodeError:
        print(f"Error: {input_file} is not a valid JSON file")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    format_ocr_data()
