from django.contrib import admin
from .models import FlashcardSet, Flashcard


class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1


@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_public", "created_at")
    inlines = [FlashcardInline]


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ("term", "flashcard_set", "order")
