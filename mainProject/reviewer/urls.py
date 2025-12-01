from django.urls import path
from . import views

app_name = 'reviewer'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject-list'),
    path('subject/<slug:slug>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('quiz/start/<int:topic_id>/', views.start_quiz, name='start-quiz'),
]
