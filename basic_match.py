import string

# Predefined technical skills list
SKILLS = {
    "python", "java", "c", "c++", "sql", "html", "css",
    "javascript", "flask", "django",
    "machine learning", "data analysis", "nlp"
}

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def extract_skills(text):
    text = clean_text(text)
    found_skills = set()

    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)

    return found_skills

# -------- SAMPLE INPUT --------
resume_text = """
Python developer with experience in Flask, SQL and Machine Learning.
"""

job_description = """
Looking for a Python developer skilled in SQL and NLP.
"""

# -------- PROCESS --------
resume_skills = extract_skills(resume_text)
jd_skills = extract_skills(job_description)

matched_skills = resume_skills & jd_skills
missing_skills = jd_skills - resume_skills

# -------- OUTPUT --------
print("Skills in Resume:", resume_skills)
print("Skills in Job Description:", jd_skills)
print("Matched Skills:", matched_skills)
print("Missing Skills:", missing_skills)
