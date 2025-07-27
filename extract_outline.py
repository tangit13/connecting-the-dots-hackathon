import fitz  # PyMuPDF
import os
import json

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    title = ""

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_text = "".join(span["text"] for span in line["spans"]).strip()
                    font_size = max(span["size"] for span in line["spans"])
                    if font_size > 20 and not title:
                        title = line_text
                    if 16 < font_size <= 20:
                        level = "H1"
                    elif 13 < font_size <= 16:
                        level = "H2"
                    elif 11 < font_size <= 13:
                        level = "H3"
                    else:
                        continue
                    headings.append({
                        "level": level,
                        "text": line_text,
                        "page": page_num + 1
                    })

    return {
        "title": title,
        "outline": headings
    }

if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            result = extract_outline(pdf_path)
            json_path = os.path.join(output_folder, filename.replace(".pdf", ".json"))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
