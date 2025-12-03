from django.urls import path
from . import views

urlpatterns = [
    path("", views.flashcard_set_list, name="flashcard_set_list"),
    path("set/new/", views.flashcard_set_create, name="flashcard_set_create"),
    path("set/<int:pk>/", views.flashcard_set_detail, name="flashcard_set_detail"),
    path("set/<int:pk>/add-card/", views.flashcard_add_card, name="flashcard_add_card"),
    path("set/<int:pk>/delete/", views.flashcard_set_delete, name="flashcard_set_delete"),
    path("card/<int:pk>/delete/", views.flashcard_delete_card, name="flashcard_delete_card"),
]
