from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from core.permissions import IsTeacher
from .models import Setbook, Chapter, Summary, Character, Theme, Quiz, Question, Choice
from .serializers import (
    SetbookSerializer,
    ChapterSerializer,
    SummarySerializer,
    CharacterSerializer,
    ThemeSerializer,
    QuizSerializer,
    QuestionSerializer,
    ChoiceSerializer,
)
import PyPDF2
import re
from . import ai_service

class SetbookViewSet(viewsets.ModelViewSet):
    queryset = Setbook.objects.all()
    serializer_class = SetbookSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'ask']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        setbook = serializer.instance
        file = setbook.file

        try:
            text = ""
            if file.name.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            else:
                text = file.read().decode('utf-8')

            # Improved chapter splitting
            chapters = re.split(r'(Chapter \d+)', text)

            # The first part is anything before "Chapter 1"
            if chapters[0].strip():
                chapter = Chapter.objects.create(setbook=setbook, title="Introduction", content=chapters[0].strip())
                ai_service.add_chapter_to_index(chapter.id, chapter.content)

            # Process the rest of the chapters
            for i in range(1, len(chapters), 2):
                title = chapters[i]
                content = chapters[i+1].strip() if (i+1) < len(chapters) else ""
                chapter = Chapter.objects.create(
                    setbook=setbook,
                    title=title.strip(),
                    content=content
                )
                ai_service.add_chapter_to_index(chapter.id, chapter.content)

        except Exception as e:
            setbook.delete()
            return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def ask(self, request, pk=None):
        setbook = self.get_object()
        question = request.data.get('question')

        if not question:
            return Response({"error": "Question not provided"}, status=status.HTTP_400_BAD_REQUEST)

        relevant_chapter_ids = ai_service.search_index(question)

        relevant_chapters_from_book = Chapter.objects.filter(
            id__in=relevant_chapter_ids,
            setbook=setbook
        )

        if not relevant_chapters_from_book:
            return Response({"answer": "I could not find any relevant information in this book to answer your question."}, status=status.HTTP_200_OK)

        relevant_content = [chapter.content for chapter in relevant_chapters_from_book]

        answer = ai_service.answer_question(question, relevant_content)

        return Response({"answer": answer}, status=status.HTTP_200_OK)

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def summarize(self, request, pk=None):
        chapter = self.get_object()
        summary_text = ai_service.summarize_text(chapter.content)

        summary = Summary.objects.create(chapter=chapter, content=summary_text)

        serializer = SummarySerializer(summary)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
    permission_classes = [permissions.IsAuthenticated]

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
