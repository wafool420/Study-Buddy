from django.contrib import admin
from .models import Subject, Topic, Question, Choice, ReviewSession

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'topic', 'created_at')
    search_fields = ('text',)

admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(ReviewSession)
