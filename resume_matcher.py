from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample resume text
resume = """
Python developer with experience in web development,
Flask, SQL, and basic machine learning.
"""

# Sample job description
job_description = """
Looking for a Python developer skilled in Flask,
SQL, and machine learning concepts.
"""

# Convert text to vectors using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform([resume, job_description])

# Calculate cosine similarity
similarity = cosine_similarity(vectors[0:1], vectors[1:2])
match_percentage = similarity[0][0] * 100

print(f"Resume Match Percentage: {match_percentage:.2f}%")
