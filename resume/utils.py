from .models import JobSkill
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import spacy
from datetime import datetime
import docx
import PyPDF2
import re
from nltk.probability import FreqDist

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
'''
def extract_text_from_pdf(file_path):
    nltk.download('punkt')
    nltk.download('punkt_tab')
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text += page.get_text()
    return text
'''    

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(len(pdf)):
            text += pdf[page_num].get_text("text")
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

'''
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
'''
def parse_experience_and_education(text):
    # Simple regex-based example for parsing
    experience_pattern = r"(experience|work history|employment history|career):?(.+?)(education|skills|$)"
    education_pattern = r"(education|academic background|qualifications):?(.+?)(experience|skills|$)"

    experience_text = re.search(experience_pattern, text, re.IGNORECASE)
    education_text = re.search(education_pattern, text, re.IGNORECASE)

    return (
        experience_text.group(2).strip() if experience_text else "",
        education_text.group(2).strip() if education_text else ""
    )
def parse_experience(text):
    # Example pattern to match roles, companies, and responsibilities
    experience_matches = re.findall(r"(?:\b(?:Manager|Engineer|Developer|Analyst|Consultant)\b.*?at\s+)([A-Za-z\s]+)\b.*?(\d{4})", text)
    experience = [{"role": role.strip(), "company": company.strip(), "year": year.strip()} for role, company, year in experience_matches]
    return experience

def parse_education(text):
    # A regex pattern that captures degree, institution, and year in various formats
    education_matches = re.findall(r"(Bachelor's|Master's|PhD|Associate's|Diploma|Certificate).*?([A-Za-z\s]+).*?(\d{4})", text, re.IGNORECASE)
    return [{"degree": degree.strip(), "institution": institution.strip(), "year": year.strip()} for degree, institution, year in education_matches]

'''
def extract_skills_from_text(text):
    # Tokenize and remove stop words
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]

    # Frequency distribution to identify common terms
    freq_dist = FreqDist(filtered_words)
    
    # Set a threshold frequency (adjust based on your text)
    common_terms = [word for word, freq in freq_dist.items() if freq > 1 and len(word) > 2]
    
    # Return unique terms as potential skills
    return list(set(common_terms))

'''    

def extract_skills_from_text(text):
    # Tokenize and remove stop words
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]

    # Frequency distribution to identify common terms
    freq_dist = FreqDist(filtered_words)
    
    # Set a threshold frequency (adjust based on your text)
    common_terms = [word for word, freq in freq_dist.items() if freq > 1 and len(word) > 2]
    
    # Return unique terms as potential skills
    return list(set(common_terms))