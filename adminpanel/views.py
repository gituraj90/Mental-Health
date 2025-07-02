

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from healthapp.models import MentalHealthSubmission

from .forms import SignUpForm, LoginForm
from healthapp.models import YouTubeVideo
from .models import ChatRecord



from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from accounts.models import ClientProfile
from adminpanel.models import ChatRecord

from django.db.models import Count
from django.db.models import Max

def signup_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('admin_dashboard')
    return render(request, 'adminpanel/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('admin_dashboard')
    return render(request, 'adminpanel/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('admin_login')

@login_required
def dashboard(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        if link:
            YouTubeVideo.objects.create(link=link)
            return redirect('admin_dashboard')

    videos = YouTubeVideo.objects.all().order_by('-added_on')
    return render(request, 'adminpanel/dashboard.html', {'videos': videos})

@login_required(login_url='login')
@csrf_protect
def remove_video(request, video_id):
    if request.method == 'POST':
        video = YouTubeVideo.objects.get(id=video_id)
        video.delete()
    return redirect('admin_dashboard')  # ✅ Correct name from urls.py


def admin_forms_view(request):
    submissions = MentalHealthSubmission.objects.all()
    return render(request, 'adminpanel/forms.html', {'submissions': submissions})

def logout_view(request):
    logout(request)
    return redirect('admin_login')

def chat_records_view(request):
    records = ChatRecord.objects.all().order_by('-timestamp')
    return render(request, 'adminpanel/chat_records.html', {'records': records})


User = get_user_model()

def client_users_list(request):
    users = User.objects.filter(is_staff=False)
    return render(request, 'adminpanel/client_users_list.html', {'users': users})

def client_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = ClientProfile.objects.get(user=user)
    chats = ChatRecord.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'adminpanel/client_user_detail.html', {
        'user_obj': user,
        'profile': profile,
        'chats': chats,
    })



@login_required
def anonymous_sessions(request):
    sessions = ChatRecord.objects.filter(user__isnull=True, session_id__isnull=False).values(
        'session_id', 'guest_name'
    ).annotate(
        total_messages=Count('id'),
        last_message=Max('timestamp')
    ).order_by('-last_message')

    return render(request, 'adminpanel/anonymous_sessions.html', {'sessions': sessions})


@login_required
def anonymous_chat_detail(request, session_id):
    records = ChatRecord.objects.filter(session_id=session_id).order_by('timestamp')
    guest_name = records.first().guest_name if records.exists() else 'Unknown'
    return render(request, 'adminpanel/anonymous_chat_detail.html', {
        'records': records,
        'guest_name': guest_name,
        'session_id': session_id
    })




from django.shortcuts import render, redirect
from .forms import GalleryItemForm
from .models import GalleryItem

def gallery_upload_view(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery_upload')  # Redirect to same page after saving
    else:
        form = GalleryItemForm()
    
    gallery_items = GalleryItem.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/gallery.html', {'form': form, 'gallery_items': gallery_items})


def delete_gallery_item(request, item_id):
    item = get_object_or_404(GalleryItem, id=item_id)
    item.delete()
    return redirect('gallery_upload')




from django.shortcuts import render, redirect
from .models import CKEditorContent
from .forms import CKEditorContentForm

def ck_editor_admin(request):
    content = CKEditorContent.objects.first()
    if request.method == 'POST':
        form = CKEditorContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('ck_editor_admin')
    else:
        form = CKEditorContentForm(instance=content)

    return render(request, 'adminpanel/ck_editor_admin.html', {'form': form})




from accounts.models import SupportPost

def support_admin_view(request):
    posts = SupportPost.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/support_posts_admin.html', {'posts': posts})




