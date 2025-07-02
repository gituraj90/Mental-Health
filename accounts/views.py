from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ClientSignUpForm, ClientProfileForm
from django.contrib.auth.decorators import login_required
from .models import ClientProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings


def signup_view(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            ClientProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender']
            )
            login(request, user)
            return redirect('home')
    else:
        form = ClientSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Manually set a different session cookie name
            request.session.set_expiry(0)  # optional: session expires on browser close
            response = redirect('home')
            response.set_cookie(
                key='client_sessionid',
                value=request.session.session_key,
                max_age=settings.SESSION_COOKIE_AGE,
                httponly=True,
                secure=settings.SESSION_COOKIE_SECURE,
                samesite='Lax',
            )
            return response
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    response = redirect('home')
    response.delete_cookie('client_sessionid')
    return response

@login_required
def profile_view(request):
    profile = ClientProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
    else:
        form = ClientProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SupportPost, SupportReply
from .forms import SupportPostForm, SupportReplyForm

from django.core.paginator import Paginator

@login_required(login_url='/accounts/login/')
def support_forum(request):
    all_posts = SupportPost.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    form = SupportPostForm()
    if request.method == 'POST':
        form = SupportPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('support_forum')

    return render(request, 'accounts/support_forum.html', {'posts': posts, 'form': form})


from django.core.paginator import Paginator

@login_required(login_url='/accounts/login/')
def support_post_detail(request, post_id):
    post = get_object_or_404(SupportPost, id=post_id)
    all_replies = post.replies.all().order_by('created_at')
    paginator = Paginator(all_replies, 5)  # 5 replies per page
    page_number = request.GET.get('page')
    replies = paginator.get_page(page_number)

    form = SupportReplyForm()
    if request.method == 'POST':
        form = SupportReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.save()
            return redirect('support_post_detail', post_id=post.id)

    return render(request, 'accounts/support_post_detail.html', {'post': post, 'replies': replies, 'form': form})


