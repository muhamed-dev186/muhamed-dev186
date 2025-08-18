from rest_framework import serializers
from .models import Setbook, Chapter, Summary, Character, Theme, Quiz, Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'choices')

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'questions')

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'name', 'description')

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'name', 'description')

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ('id', 'content', 'created_at')

class ChapterSerializer(serializers.ModelSerializer):
    summaries = SummarySerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'content', 'summaries')

class SetbookSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    themes = ThemeSerializer(many=True, read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Setbook
        fields = ('id', 'title', 'author', 'file', 'uploaded_by', 'chapters', 'themes', 'characters', 'quizzes')
