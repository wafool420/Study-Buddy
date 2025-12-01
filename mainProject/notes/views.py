from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Note
from .forms import NoteForm


@login_required
def note_list(request):
    # Only show notes belonging to the logged-in user
    profile = request.user.profile
    notes = Note.objects.filter(user=request.user).order_by("-updated_at")

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user          # attach the owner
            note.save()
            return redirect("note_detail", pk=note.pk)
    else:
        form = NoteForm()

    return render(
        request,
        "notes/note_list.html",
        {
            "notes": notes,
            "form": form,
        },
    )


@login_required
def note_detail(request, pk):
    # User can only access their own note
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "notes/note_detail.html",
        {
            "note": note,
            "form": form,
        },
    )


@login_required
def note_delete(request, pk):
    # Again, note must belong to the current user
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "POST":
        note.delete()
        return redirect("note_list")

    return render(
        request,
        "notes/note_confirm_delete.html",
        {"note": note},
    )
