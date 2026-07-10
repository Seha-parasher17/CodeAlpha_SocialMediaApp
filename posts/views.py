from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, PostForm
from .models import Comment, Post

def home(request):
    posts = Post.objects.select_related("author", "author__profile").prefetch_related(
        "likes",
        Prefetch("comments", queryset=Comment.objects.select_related("author")),
    )
    return render(request, "posts/home.html", {"posts": posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created.")
            return redirect("posts:home")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related("author", "author__profile").prefetch_related("likes", "comments__author"),
        pk=pk,
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("posts:post_detail", pk=post.pk)
    else:
        form = CommentForm()

    return render(request, "posts/post_detail.html", {"post": post, "form": form})

@login_required
def toggle_like(request, pk):
    if request.method != "POST":
        return redirect("posts:post_detail", pk=pk)

    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(request.POST.get("next") or "posts:home")
