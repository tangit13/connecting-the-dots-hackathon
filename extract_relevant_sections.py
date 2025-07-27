import os
import fitz
import json
from sentence_transformers import SentenceTransformer, util
from datetime import datetime

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        for para in text.split("\n\n"):
            clean = para.strip().replace("\n", " ")
            if len(clean) > 50:
                sections.append({"text": clean, "page": page_num + 1})
    return sections

def rank_sections(sections, persona, job, model):
    scores = []
    combined_query = persona + " " + job
    query_embedding = model.encode(combined_query, convert_to_tensor=True)
    for section in sections:
        section_embedding = model.encode(section["text"], convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, section_embedding).item()
        scores.append((score, section))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [{"importance_rank": i+1, "page": s["page"], "section_title": s["text"][:80], "refined_text": s["text"]} for i, (score, s) in enumerate(scores[:10])]

def build_final_output(input_files, persona, job):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    all_sections = []
    for fname in input_files:
        path = os.path.join("input", fname)
        sections = extract_sections(path)
        ranked = rank_sections(sections, persona, job, model)
        all_sections.extend([dict(doc=fname, **s) for s in ranked])
    return {
        "docs": input_files,
        "persona": persona,
        "job": job,
        "timestamp": datetime.now().isoformat(),
        "results": all_sections
    }

if __name__ == "__main__":
    persona = open("persona.txt", encoding="utf-8").read()
    job = open("job.txt", encoding="utf-8").read()
    input_files = [f for f in os.listdir("input") if f.endswith(".pdf")]
    final_output = build_final_output(input_files, persona, job)
    with open("output/ranked_sections.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
