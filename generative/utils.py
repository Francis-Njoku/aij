import openai
from django.conf import settings
import fitz  # PyMuPDF for PDF files
from docx import Document  # python-docx for DOCX files

openai.api_key = settings.OPENAI_API_KEY

def generate_interview_questions(skills):
    # Generate a prompt based on the skills
    skill_text = ','.join(skills)
    prompt = (
        f"Generate at least 10 interview questions (both technical and non-technical) for a candidate skilled in {skill_text}. "
        "Provide 5 technical questions focused on their expertise in these skills, and 5 non-technical questions that assess "
        "soft skills, problem-solving, teamwork, and adaptability. Include model answers for each question."
    )

    try:
        # Call OpenAI's GPT model
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip() if response.choices else ""
    
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Error generating interview questions. Please try again later."
    
def generate_cover_letter(resume_text, job_title, company_name, job_description):
    prompt = (
        f"Generate a professional cover letter for a candidate applying to the position of {job_title} at {company_name}. "
        f"The candidate's skills, experience, and achievements are as follows:\n{resume_text}\n"
        f"The job description includes the following requirements and responsibilities:\n{job_description}\n"
        "Write a cover letter that highlights the candidate's fit for the role, emphasizing relevant skills and experience."
    )

    try:
        # Call OpenAI API to generate the cover letter
        response = openai.Completion.create(
            model="text-davinci-003",  # Or another suitable model like gpt-3.5-turbo
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Return the generated cover letter text
        return response.choices[0].text.strip() if response.choices else ""
    
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Error generating cover letter. Please try again later."    
    
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_doc(doc_path):
    text = ""
    try:
        doc = Document(doc_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOC: {e}")
    return text    