# interview/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_interview_questions, generate_cover_letter, extract_text_from_doc, extract_text_from_pdf
from .models import InterviewQuestion, CoverLetter
from .serializers import InterviewQuestionSerializer, CoverLetterSerializer
from django.contrib.auth.models import User


class UserInterviewQuestionsView(ListAPIView):
    serializer_class = InterviewQuestionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return InterviewQuestion.objects.filter(user_id=user_id)
    
class InterviewQuestionView(APIView):
    def post(self, request):
        skills = request.data.get('skills', [])
        user_id = request.data.get('user_id')  # Ensure the user ID is passed in the request

        if not skills or not user_id:
            return Response({"error": "Skills and user ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the user instance
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate questions and answers
        questions_and_answers_text = generate_interview_questions(skills)
        skill_text = ', '.join(skills)

        # Parse the questions and answers
        questions_and_answers_list = questions_and_answers_text.split("\n\n")
        questions_and_answers = []

        for qa in questions_and_answers_list:
            parts = qa.split("\nA: ")
            if len(parts) == 2:
                question = parts[0].replace("Q: ", "")
                answer = parts[1]
                questions_and_answers.append((question, answer))

                # Save each question and answer in the database
                InterviewQuestion.objects.create(
                    user=user,
                    skill=skill_text,
                    question=question,
                    answer=answer
                )

        # Serialize the saved questions and answers to return in the response
        saved_questions = InterviewQuestion.objects.filter(user=user, skill=skill_text)
        serializer = InterviewQuestionSerializer(saved_questions, many=True)

        return Response({"questions_and_answers": serializer.data}, status=status.HTTP_201_CREATED)
    
class GenerateCoverLetterView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        job_title = request.data.get('job_title')
        company_name = request.data.get('company_name')
        job_description = request.data.get('job_description')

        # Validate input data
        if not all([user_id, job_title, company_name, job_description]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get user instance
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the latest resume for the user
        try:
            latest_resume = Resume.objects.filter(user=user).latest('uploaded_at')
        except Resume.DoesNotExist:
            return Response({"error": "No resume found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Determine file type and extract text
        resume_text = ""
        file_extension = os.path.splitext(latest_resume.file.name)[1].lower()

        try:
            if file_extension == '.pdf':
                resume_text = extract_text_from_pdf(latest_resume.file.path)
            elif file_extension in ['.doc', '.docx']:
                resume_text = extract_text_from_doc(latest_resume.file.path)
            else:
                return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error reading resume file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Generate the cover letter
        cover_letter_text = generate_cover_letter(resume_text, job_title, company_name, job_description)

        # Save the cover letter in the database
        cover_letter = CoverLetter.objects.create(
            user=user,
            job_title=job_title,
            company_name=company_name,
            cover_letter_text=cover_letter_text
        )

        # Serialize the saved cover letter for response
        serializer = CoverLetterSerializer(cover_letter)
        return Response(serializer.data, status=status.HTTP_201_CREATED)