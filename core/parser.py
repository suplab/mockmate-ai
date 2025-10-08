# core/parser.py
import fitz  # PyMuPDF
from docx import Document
from typing import Dict
import re
import os

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text_chunks = []
    for page in doc:
        text_chunks.append(page.get_text())
    return "\n".join(text_chunks)

def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)

def parse_resume_file(uploaded_file) -> Dict:
    """Accepts a Streamlit uploaded file-like object.
    Returns a dictionary with raw_text and simple heuristics (name, emails, skills).
    """
    filename = uploaded_file.name
    data = uploaded_file.read()
    tmp_dir = '/tmp/mockmate'
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_path = os.path.join(tmp_dir, filename)
    with open(tmp_path, "wb") as f:
        f.write(data)

    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(tmp_path)
    elif filename.lower().endswith(('.docx', '.doc')):
        text = extract_text_from_docx(tmp_path)
    else:
        try:
            text = data.decode('utf-8')
        except Exception:
            text = ""

    # heuristics
    name = None
    email = None
    phones = []
    skills = []

    # name: first non-empty line, heuristically
    for line in text.splitlines():
        s = line.strip()
        if s:
            if len(s.split()) <= 5:
                name = s
            break

    m = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    if m:
        email = m.group(0)

    # Indian phone number patterns: +91xxxxxxxxxx, 0xxxxxxxxxx, xxxxxxxxxx starting with 6-9
    phones_raw = re.findall(r"(?:\+91[ -]?)?[6-9][0-9]{9}|0[6-9][0-9]{9}", text)
    normalized = []
    for p in phones_raw:
        normalized.append(p.replace(' ', '').replace('-', ''))
    phones = list(sorted(set(normalized)))

    # skills
    SKILL_KEYWORDS = [
        'python', 'java', 'spring', 'spring boot', 'spring-boot', 'aws', 'docker', 'kubernetes', 'sql', 'postgres',
        'numpy', 'pandas', 'tensorflow', 'pytorch', 'react', 'node', 'ml', 'data', 'api', 'rest', 'rest api', 'microservices',
        'as400', 'rpgle', 'ibmi', 'synon', 'ibm i', 'ibm-i',
        'project management', 'team mentoring', 'stakeholder management', 'agile delivery', 'requirement estimation', 'delivery planning'
    ]
    text_lower = text.lower()
    for kw in SKILL_KEYWORDS:
        if kw in text_lower:
            skills.append(kw)

    return {
        'filename': filename,
        'raw_text': text,
        'name': name,
        'email': email,
        'phones': phones,
        'skills': list(sorted(set(skills)))
    }
