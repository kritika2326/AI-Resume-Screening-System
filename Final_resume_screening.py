import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- SKILL LIST ----------------
SKILLS = {
    "python", "java", "c", "c++", "sql", "html", "css",
    "javascript", "flask", "django",
    "machine learning", "data analysis", "nlp"
}

# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    text = clean_text(text)
    found_skills = set()
    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)
    return found_skills

# ---------------- SIMILARITY CALCULATION ----------------
def calculate_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity * 100

# ---------------- SAMPLE INPUT ----------------
resume_text = """
Python developer with experience in Flask, SQL, C and Machine Learning.
"""

job_description = """
Looking for a Python developer skilled in SQL and NLP.
"""

# ---------------- PROCESS ----------------
match_percentage = calculate_similarity(resume_text, job_description)

resume_skills = extract_skills(resume_text)
jd_skills = extract_skills(job_description)

matched_skills = resume_skills & jd_skills
missing_skills = jd_skills - resume_skills

# ---------------- OUTPUT ----------------
print(f"\nResume Match Percentage: {match_percentage:.2f}%\n")

print("Skills in Resume:", resume_skills)
print("Skills in Job Description:", jd_skills)
print("Matched Skills:", matched_skills)
print("Missing Skills:", missing_skills)
