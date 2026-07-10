from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProfileForm, RegisterForm

def register(request):
    if request.user.is_authenticated:
        return redirect("posts:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("posts:home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    posts = profile_user.posts.select_related("author").prefetch_related("likes", "comments")
    is_following = profile.followers.filter(id=request.user.id).exists()

    return render(
        request,
        "accounts/profile_detail.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "posts": posts,
            "is_following": is_following,
        },
    )

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})

@login_required
def toggle_follow(request, username):
    if request.method != "POST":
        return redirect("accounts:profile", username=username)

    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect("accounts:profile", username=username)

    profile = target_user.profile
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)

    return redirect("accounts:profile", username=username)
