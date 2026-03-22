from flask import Flask, render_template, request
import PyPDF2
import docx
import os

app = Flask(__name__)

# -------------------------------
# EXTRACT TEXT FROM PDF
# -------------------------------
def extract_pdf(file):
    text = ""
    try:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content
    except:
        text = ""
    return text


# -------------------------------
# EXTRACT TEXT FROM DOCX
# -------------------------------
def extract_docx(file):
    text = ""
    try:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "
    except:
        text = ""
    return text


# -------------------------------
# HOME ROUTE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        if "resume" not in request.files:
            return render_template("index.html")

        file = request.files["resume"]

        if file.filename == "":
            return render_template("index.html")

        filename = file.filename.lower()

        # -------------------------------
        # READ FILE
        # -------------------------------
        if filename.endswith(".pdf"):
            resume_text = extract_pdf(file)
        elif filename.endswith(".docx"):
            resume_text = extract_docx(file)
        else:
            return render_template("index.html")

        resume_text = resume_text.lower()

        # -------------------------------
        # SKILL DOMAINS
        # -------------------------------
        domains = {
            "Data Analyst": ["python", "sql", "excel", "power bi", "tableau"],
            "Data Scientist": ["python", "machine learning", "pandas", "numpy"],
            "Frontend Developer": ["html", "css", "javascript", "react"],
            "Backend Developer": ["python", "java", "django", "flask"],
            "Full Stack Developer": ["html", "css", "javascript", "node", "mongodb"],
            "Cybersecurity": ["network security", "ethical hacking"],
            "Cloud Engineer": ["aws", "azure", "docker"],
            "DevOps Engineer": ["jenkins", "docker", "kubernetes"],
            "Finance Analyst": ["accounting", "excel", "finance"],
            "Marketing": ["seo", "digital marketing"],
            "HR": ["recruitment", "communication"]
        }

        best_role = "No strong match found"
        best_score = 0
        best_matched = []
        best_missing = []

        # -------------------------------
        # FIND BEST ROLE
        # -------------------------------
        for role, skills in domains.items():

            matched = []
            for skill in skills:
                if skill in resume_text:
                    matched.append(skill)

            score = int((len(matched) / len(skills)) * 100)

            if score > best_score:
                best_score = score
                best_role = role
                best_matched = matched
                best_missing = list(set(skills) - set(matched))

        # -------------------------------
        # EVALUATION MESSAGE
        # -------------------------------
        if best_score >= 80:
            evaluation = "Excellent match! You're job-ready 🎯"
        elif best_score >= 60:
            evaluation = "Good match 👍 Improve a few skills"
        else:
            evaluation = "Needs improvement ⚠️ Focus on missing skills"

        return render_template(
            "index.html",
            percentage=best_score,
            matched=best_matched,
            missing=best_missing,
            evaluation=evaluation,
            role=best_role
        )

    return render_template("index.html")


# -------------------------------
# RUN APP (IMPORTANT FOR DEPLOY)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)