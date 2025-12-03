from django.urls import path
from . import views

app_name = "reviewer"

urlpatterns = [
    # SUBJECTS
    path("", views.SubjectListView.as_view(), name="subject-list"),
    path("subject/new/", views.subject_create, name="subject-create"),
    path(
        "subject/<slug:slug>/",
        views.SubjectDetailView.as_view(),
        name="subject-detail",
    ),
    path(
        "subject/<slug:slug>/delete/",
        views.subject_delete,
        name="subject-delete",
    ),

    # TOPICS
    path(
        "subject/<slug:subject_slug>/topic/new/",
        views.topic_create,
        name="topic-create",
    ),
    path(
        "topic/<int:pk>/",
        views.TopicDetailView.as_view(),
        name="topic-detail",
    ),
    path(
        "topic/<int:pk>/delete/",
        views.topic_delete,
        name="topic-delete",
    ),

    # QUESTIONS / QUIZ
    path(
        "quiz/start/<int:topic_id>/",
        views.start_quiz,
        name="start-quiz",
    ),
    path(
        "topic/<int:topic_id>/question/new/",
        views.question_create,
        name="question-create",
    ),
    path(
        "question/<int:pk>/delete/",
        views.question_delete,
        name="question-delete",
    ),

    # (optional later) path("question/<int:pk>/delete/", views.question_delete, name="question-delete"),
]
