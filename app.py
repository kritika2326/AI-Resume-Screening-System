from flask import Flask, render_template, request
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ---------------- SKILLS SET ----------------
SKILLS = {
    # Programming Languages
    "python", "java", "c++", "c#", "rust",

    # Web Development
    "html", "css", "javascript", "react", "node", "flask", "django",

    # Databases
    "sql", "mysql", "postgresql", "mongodb",

    # Data & AI
    "machine learning", "deep learning", "nlp", "data analysis",
    "pandas", "numpy", "scikit-learn",

    # Tools & Platforms
    "git", "github", "docker", "linux",

    # Cloud & DevOps
    "aws", "azure", "ci/cd",
    "CI/CD pipelines"
}

# ---------------- NEGATIONS ----------------
NEGATIONS = {
    "no", "not", "never", "without",
    "no experience", "never used",
    "dont", "do not", "did not"
}

# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = text.lower()
    # Replace punctuation with spaces (CRITICAL FIX)
    text = re.sub(r"[^\w\s]", " ", text)
    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    text = clean_text(text)
    found = set()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        for match in re.finditer(pattern, text):
            before_start = max(0, match.start() - 7)
            after_end = min(len(text), match.end() + 7)

            before_context = text[before_start:match.start()]
            after_context = text[match.end():after_end]

            context = before_context + " " + after_context

            if not any(neg in context for neg in NEGATIONS):
                found.add(skill)

    return found
# ---------------- TF-IDF (OPTIONAL METRIC) ----------------
def calculate_similarity(resume, jd):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

# ---------------- JOB-WEIGHTED MATCH % ----------------
def skill_match_percentage(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0
    return round((len(resume_skills & jd_skills) / len(jd_skills)) * 100, 2)

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resume_text = ""
    job_text = ""

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "")
        job_text = request.form.get("job_text", "")

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(job_text)

        match = skill_match_percentage(resume_skills, jd_skills)

        result = {
            "match": match,
            "resume_skills": sorted(resume_skills),
            "jd_skills": sorted(jd_skills),
            "matched": sorted(resume_skills & jd_skills),
            "missing": sorted(jd_skills - resume_skills)
        }

    return render_template(
    "index.html",
    result=result,
    resume_text=resume_text if request.method == "POST" else "",
    jd_text=job_text if request.method == "POST" else ""
)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
