from docx import Document
import json

INPUT_FILE = "Uzbek tarix  RUS.docx"
OUTPUT_FILE = "questions.json"

doc = Document(INPUT_FILE)
text = "\n".join(p.text for p in doc.paragraphs)

blocks = text.split("+++++")

questions = []

for block in blocks:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    if len(lines) < 5:
        continue

    question = lines[0]
    options = []
    correct_index = None

    for line in lines[1:]:
        if line.startswith("@"):
            correct_index = len(options)
            options.append(line[1:].strip())
        elif not line.startswith("="):
            options.append(line.strip())

    if correct_index is None or len(options) != 4:
        continue

    questions.append({
        "question": question,
        "options": options,
        "correct": correct_index
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Готово! Вопросов: {len(questions)}")
