from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FlashcardForm, FlashcardSetForm
from .models import FlashcardSet, Flashcard


@login_required
def flashcard_set_list(request):
    active_tab = request.GET.get("tab", "yours")
    if active_tab not in ("yours", "browse"):
        active_tab = "yours"

    my_sets = FlashcardSet.objects.filter(owner=request.user)
    public_sets = FlashcardSet.objects.filter(is_public=True).exclude(owner=request.user)

    context = {
        "my_sets": my_sets,
        "public_sets": public_sets,
        "active_tab": active_tab,
    }
    return render(request, "set_list.html", context)


def flashcard_set_detail(request, pk):
    flashcard_set = get_object_or_404(FlashcardSet, pk=pk)
    cards = flashcard_set.cards.all().order_by("order", "id")

    is_owner = (
        request.user.is_authenticated
        and request.user == flashcard_set.owner
    )

    return render(
        request,
        "set_detail.html",
        {
            "set": flashcard_set,
            "cards": cards,
            "is_owner": is_owner,
        },
    )


@login_required
def flashcard_set_create(request):
    if request.method == "POST":
        form = FlashcardSetForm(request.POST)
        if form.is_valid():
            flashcard_set = form.save(commit=False)
            flashcard_set.owner = request.user
            flashcard_set.save()

            # create cards from term/definition
            terms = request.POST.getlist("term")
            defs = request.POST.getlist("definition")
            order = 0
            for term, definition in zip(terms, defs):
                term = term.strip()
                definition = definition.strip()
                if term or definition:
                    Flashcard.objects.create(
                        flashcard_set=flashcard_set,
                        term=term or "(no term)",
                        definition=definition or "(no definition yet)",
                        order=order,
                    )
                    order += 1

            # decide where to go based on which button was clicked
            action = request.POST.get("action")
            if action == "create":
                # just go back to list
                return redirect("flashcard_set_list")
            else:
                # default: go to set detail to practice
                return redirect("flashcard_set_detail", pk=flashcard_set.pk)
    else:
        form = FlashcardSetForm()

    return render(request, "set_form.html", {"form": form})




@login_required
def flashcard_add_card(request, pk):
    flashcard_set = get_object_or_404(FlashcardSet, pk=pk, owner=request.user)

    if request.method == "POST":
        form = FlashcardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.flashcard_set = flashcard_set
            card.order = flashcard_set.cards.count()
            card.save()
            return redirect("flashcard_set_detail", pk=flashcard_set.pk)
    else:
        form = FlashcardForm()

    return render(
        request,
        "card_form.html",
        {"form": form, "set": flashcard_set},
    )

login_required
def flashcard_set_delete(request, pk):
    flashcard_set = get_object_or_404(FlashcardSet, pk=pk, owner=request.user)

    if request.method == "POST":
        flashcard_set.delete()
        return redirect("flashcard_set_list")

    # simple confirm page (optional)
    return render(request, "set_detail.html", {"set": flashcard_set})


@login_required
def flashcard_delete_card(request, pk):
    card = get_object_or_404(
        Flashcard,
        pk=pk,
        flashcard_set__owner=request.user,
    )
    set_pk = card.flashcard_set.pk

    if request.method == "POST":
        card.delete()
        return redirect("flashcard_set_detail", pk=set_pk)

    # optional: simple confirm page
    return render(
        request,
        "flashcards/card_confirm_delete.html",
        {"card": card, "set": card.flashcard_set},
    )

