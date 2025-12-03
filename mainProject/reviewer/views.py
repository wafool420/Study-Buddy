from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Subject, Topic, Question, Choice, ReviewSession
from .forms import SubjectForm, TopicForm, QuestionForm, ChoiceFormSet
import random

class SubjectListView(ListView):
    model = Subject
    template_name = "reviewer/subject_list.html"
    context_object_name = "subjects"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        request = self.request

        tab = request.GET.get("tab", "yours")
        if not request.user.is_authenticated:
            tab = "browse"
        ctx["active_tab"] = tab

        if request.user.is_authenticated:
            ctx["my_subjects"] = Subject.objects.filter(
                owner=request.user
            ).order_by("-created_at")

            ctx["browse_subjects"] = Subject.objects.filter(
                is_public=True
            ).order_by("-created_at")
        else:
            ctx["my_subjects"] = Subject.objects.none()
            ctx["browse_subjects"] = Subject.objects.filter(
                is_public=True
            ).order_by("-created_at")

        return ctx



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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        topic = self.object
        ctx["question_count"] = topic.questions.count()
        ctx["is_owner"] = (
            self.request.user.is_authenticated
            and topic.subject.owner == self.request.user
        )
        return ctx


@login_required
def question_create(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # save question
            question = form.save(commit=False)
            question.topic = topic
            question.save()

            # attach choices
            formset.instance = question
            formset.save()

            return redirect("reviewer:topic-detail", pk=topic.pk)

        # DEBUG: print any errors to console so you can see them
        print("QUESTION ERRORS:", form.errors)
        print("CHOICE ERRORS:", formset.errors)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    return render(
        request,
        "reviewer/question_form.html",
        {"topic": topic, "form": form, "formset": formset},
    )



@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user   # if you have owner field
            subject.save()
            return redirect("reviewer:subject-detail", slug=subject.slug)
        # IMPORTANT: if not valid, we just fall through and
        # render the same *bound* form with errors
    else:
        form = SubjectForm()

    return render(request, "reviewer/subject_form.html", {"form": form})


def start_quiz(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if not topic.questions.exists():
        return redirect('reviewer:topic-detail', pk=topic.pk)

    questions = list(topic.questions.all())
    random.shuffle(questions)
    questions = questions[:5]

    # 👇 add this
    is_owner = (
        request.user.is_authenticated
        and topic.subject.owner == request.user
    )

    if request.method == 'POST':
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

        ReviewSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            subject=topic.subject,
            score=score,
            total=total,
        )

        return render(
            request,
            'reviewer/quiz_result.html',
            {
                'score': score,
                'total': total,
                'topic': topic,
                'is_owner': is_owner,
            },
        )

    return render(
        request,
        'reviewer/quiz_start.html',
        {
            'topic': topic,
            'questions': questions,
            'is_owner': is_owner,
        },
    )


@login_required
def topic_create(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)

    # only the owner can add topics
    if subject.owner != request.user:
        return HttpResponseForbidden("You do not own this reviewer.")

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.save()
            return redirect("reviewer:subject-detail", slug=subject.slug)
    else:
        form = TopicForm()

    return render(
        request,
        "reviewer/topic_form.html",
        {"subject": subject, "form": form},
    )

@require_POST
@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    # only the subject owner can delete
    if topic.subject.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this topic.")

    subject_slug = topic.subject.slug
    topic.delete()
    return redirect("reviewer:subject-detail", slug=subject_slug)

@require_POST
@login_required
def subject_delete(request, slug):
    subject = get_object_or_404(Subject, slug=slug)

    # only the owner can delete
    if subject.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this reviewer.")

    subject.delete()
    return redirect("reviewer:subject-list")

@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # Adjust this line to whatever field actually stores the owner
    owner = question.topic.subject.owner

    if request.user != owner:
        return HttpResponseForbidden("You are not allowed to delete this question.")

    topic_id = question.topic.id

    if request.method == "POST":
        question.delete()
        return redirect("reviewer:start-quiz", topic_id=topic_id)

    # If someone hits the URL with GET, just send them back
    return redirect("reviewer:start-quiz", topic_id=topic_id)