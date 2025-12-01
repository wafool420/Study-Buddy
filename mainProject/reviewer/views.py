from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Subject, Topic, Question, Choice, ReviewSession
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class SubjectListView(ListView):
    model = Subject
    template_name = 'reviewer/subject_list.html'
    context_object_name = 'subjects'

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'reviewer/subject_detail.html'
    context_object_name = 'subject'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'reviewer/topic_detail.html'
    context_object_name = 'topic'

import random
from django.urls import reverse

def start_quiz(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    questions = list(topic.questions.all())
    # pick N random questions (or all)
    random.shuffle(questions)
    questions = questions[:5]  # change as needed

    if request.method == 'POST':
        # process answers
        user_answers = {}
        correct = 0
        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            if choice_id:
                try:
                    choice = Choice.objects.get(pk=int(choice_id))
                    if choice.is_correct:
                        correct += 1
                except Choice.DoesNotExist:
                    pass
        total = len(questions)
        score = correct
        session = ReviewSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            subject=topic.subject,
            score=score,
            total=total
        )
        return render(request, 'reviewer/quiz_result.html', {'score': score, 'total': total, 'topic': topic})
    else:
        return render(request, 'reviewer/quiz_start.html', {'topic': topic, 'questions': questions})
