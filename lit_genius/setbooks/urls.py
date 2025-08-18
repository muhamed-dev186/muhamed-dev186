from django.urls import path
from .views import (
    SetbookViewSet,
    ChapterViewSet,
    SummaryViewSet,
    CharacterViewSet,
    ThemeViewSet,
    QuizViewSet,
    QuestionViewSet,
    ChoiceViewSet,
)

setbook_list = SetbookViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

setbook_detail = SetbookViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

chapter_list = ChapterViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

chapter_detail = ChapterViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

summary_list = SummaryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

summary_detail = SummaryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

character_list = CharacterViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

character_detail = CharacterViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

theme_list = ThemeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

theme_detail = ThemeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

quiz_list = QuizViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

quiz_detail = QuizViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

question_list = QuestionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

question_detail = QuestionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

choice_list = ChoiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

choice_detail = ChoiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('setbooks/', setbook_list, name='setbook-list'),
    path('setbooks/<int:pk>/', setbook_detail, name='setbook-detail'),
    path('setbooks/<int:pk>/ask/', SetbookViewSet.as_view({'post': 'ask'}), name='setbook-ask'),
    path('chapters/', chapter_list, name='chapter-list'),
    path('chapters/<int:pk>/', chapter_detail, name='chapter-detail'),
    path('chapters/<int:pk>/summarize/', ChapterViewSet.as_view({'post': 'summarize'}), name='chapter-summarize'),
    path('summaries/', summary_list, name='summary-list'),
    path('summaries/<int:pk>/', summary_detail, name='summary-detail'),
    path('characters/', character_list, name='character-list'),
    path('characters/<int:pk>/', character_detail, name='character-detail'),
    path('themes/', theme_list, name='theme-list'),
    path('themes/<int:pk>/', theme_detail, name='theme-detail'),
    path('quizzes/', quiz_list, name='quiz-list'),
    path('quizzes/<int:pk>/', quiz_detail, name='quiz-detail'),
    path('questions/', question_list, name='question-list'),
    path('questions/<int:pk>/', question_detail, name='question-detail'),
    path('choices/', choice_list, name='choice-list'),
    path('choices/<int:pk>/', choice_detail, name='choice-detail'),
]
