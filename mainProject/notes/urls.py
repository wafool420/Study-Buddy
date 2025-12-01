from django.urls import path
from . import views

urlpatterns = [
    # 1. Main List
    path('', views.note_list, name='note_list'),
    
    # 2. Create Note
    path('new/', views.note_detail, name='create_note'),

    # 3. Edit Note
    path('<int:pk>/', views.note_detail, name='note_detail'),

    # 4. Delete Note (THIS WAS THE ISSUE)
    # The name here must match the {% url 'note_delete' ... %} in your HTML
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
]