from .models import JobSkill
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import spacy
from datetime import datetime

# Download necessary nltk data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

nlp = spacy.load("en_core_web_sm")


def get_job_skills_from_db():
    return set(skill.name.lower() for skill in JobSkill.objects.all())

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

    job_skills = get_job_skills_from_db()
    matched_keywords = set(words).intersection(job_skills)
    return list(matched_keywords)

def extract_text_from_pdf(file_path):
    nltk.download('punkt')
    nltk.download('punkt_tab')
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text += page.get_text()
    return text

def parse_experience_and_education(text):
    doc = nlp(text)
    experience = []
    education = []

    # For simplicity, look for specific keywords to divide sections
    sections = {'experience': [], 'education': []}
    current_section = None
    
    for sentence in doc.sents:
        line = sentence.text.lower()
        
        if "experience" in line or "work" in line:
            current_section = "experience"
        elif "education" in line:
            current_section = "education"
        
        if current_section:
            sections[current_section].append(line)

    # Post-process sections to fill education and experience
    experience = "\n".join(sections['experience'])
    education = "\n".join(sections['education'])

    return experience, education