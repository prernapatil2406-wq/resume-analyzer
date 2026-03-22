from docx import Document
import pdfplumber

# Extract text from resume
def extract_text(file):

    text = ""

    # DOCX file
    if file.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    # PDF file
    elif file.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    # TXT file
    elif file.endswith(".txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

    else:
        text = "Unsupported file format"

    return text.lower()


# Extract skills from Job Description
def extract_skills_from_jd(job_description, skills_list):

    found_skills = []

    for skill in skills_list:
        if skill.lower() in job_description.lower():
            found_skills.append(skill)

    return found_skills


# Match resume skills with job skills
def match_skills(resume_text, job_skills):

    matched = []
    missing = []

    for skill in job_skills:
        if skill.lower() in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(job_skills) > 0:
        percentage = (len(matched) / len(job_skills)) * 100
    else:
        percentage = 0

    return matched, missing, percentage