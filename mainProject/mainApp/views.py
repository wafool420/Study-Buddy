from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment
from django.contrib import messages
from .forms import ProfileForm, PostForm, CommentForm, ReplyForm


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

@login_required
def home(request):
    profile = request.user.profile
    posts = Post.objects.all()


    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = ProfileForm(instance=profile)

    return render(request, "home.html", {
        'profile': profile,
        'form': form,
        'posts': posts,
    })

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form':form,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user        # or post.post_user if that's your field
            post.save()
            return redirect('home')         # go back to feed
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)

    # only the owner of the post can delete it
    if post.user != request.user:
        raise PermissionDenied("You are not allowed to delete this post.")

    if request.method == "POST":
        post.delete()
        return redirect('home')

    # no confirmation page for now, just go back
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)   
            comment.post = post                 
            comment.user = request.user         
            comment.save()
            return redirect('home')             
    else:
        form = CommentForm()

    return render(request, "add_comment.html", {"form": form, "post": post})

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    # who is allowed?
    is_comment_owner = (comment.user == request.user)
    is_post_owner = (comment.post.user == request.user)

    if not (is_comment_owner or is_post_owner):
        # you can also just `return redirect('home')` if you don't want a 403
        raise PermissionDenied("You are not allowed to delete this comment.")

    if request.method == "POST":
        comment.delete()
        return redirect('home')

    # no GET confirmation page for now, just bounce back
    return redirect('home')

def add_reply(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment          # link reply → comment
            reply.user = request.user        # who wrote it
            reply.save()
            return redirect('home')          # back to feed
    else:
        form = ReplyForm()

    return render(request, "add_reply.html", {
        "form": form,
        "comment": comment,
    })

@login_required
def delete_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)

    # who is allowed?
    is_reply_owner = (reply.user == request.user)
    is_post_owner = (reply.comment.post.user == request.user)
    is_comment_owner = (reply.comment.user == request.user)
    # optional: allow comment owner too
    # is_comment_owner = (reply.comment.user == request.user)

    if not (is_reply_owner or is_post_owner or is_comment_owner):
        raise PermissionDenied("You are not allowed to delete this reply.")

    if request.method == "POST":
        reply.delete()
        return redirect('home')

    return redirect('home')
