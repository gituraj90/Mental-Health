
from django.shortcuts import render, redirect
from .forms import MentalHealthSurveyForm
import requests
from django.http import JsonResponse
from django.conf import settings

from .models import MentalHealthSubmission


from django.views.decorators.csrf import csrf_exempt

import json



from .models import YouTubeVideo
import google.generativeai as genai
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from adminpanel.models import ChatRecord

from uuid import uuid4








# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyACfQd7mTCA42255tan4KubAhwFzybv-AE")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")






def get_score(stress_level, diagnosed, symptoms):
    score = 0
    score += {"Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}.get(stress_level, 0)
    score += {"No": 0, "Self-diagnosed": 2, "Yes, by a professional": 3}.get(diagnosed, 0)
    score += len(symptoms)
    return score


def mental_health_form(request):
    if request.method == 'POST':
        form = MentalHealthSurveyForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            symptoms_list = form.cleaned_data['symptoms']
            stress_level = form.cleaned_data['stress_level']
            diagnosed = form.cleaned_data['diagnosed']
            other_issues = form.cleaned_data.get('other_issues', '')

            # Scoring & AI feedback
            instance.symptoms = ', '.join(symptoms_list)
            instance.total_score = get_score(stress_level, diagnosed, symptoms_list)
            
            instance.save()
            return render(request, 'healthapp/result.html', {
                'score': instance.total_score,
                'feedback': instance.ai_feedback
            })
    else:
        form = MentalHealthSurveyForm()
    
    return render(request, 'healthapp/survey_form.html', {'form': form})


def relaxing_videos(request):
    return render(request, 'healthapp/relaxing_videos.html')

def articles(request):
    return render(request, 'healthapp/articles.html')




def get_youtube_videos(request):
    api_key = settings.YOUTUBE_API_KEY  # ✅ Make sure this key is set correctly
    search_query = "mental health awareness"
    max_results = 30

    youtube_api_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&type=video&maxResults={max_results}&key={api_key}"

    response = requests.get(youtube_api_url)
    data = response.json()

    print("API Response:", data)  # ✅ Debugging print

    if "error" in data:  # ✅ If API returns an error, print it
        print("YouTube API Error:", data["error"]["message"])
        return JsonResponse({"error": data["error"]["message"]}, status=400)

    videos = []
    if "items" in data:
        for item in data["items"]:
            if "videoId" in item.get("id", {}):  # ✅ Avoid KeyError
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                thumbnail_url = item["snippet"]["thumbnails"]["medium"]["url"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                videos.append({
                    "title": title,
                    "thumbnail": thumbnail_url,
                    "video_url": video_url
                })

    print("Fetched Videos:", videos)  # ✅ Debugging print

    return JsonResponse({"videos": videos})










def generate_gemini_response(user_input):
    prompt = f"""
You are a helpful and supportive mental health assistant. 
Only respond to queries related to emotional well-being, stress, anxiety, or mental health. 
If a question is unrelated, respond: "Sorry, I can only assist with mental health-related questions."

User: {user_input}
Assistant:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Bot Error: {str(e)}"









@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            guest_name = data.get("guest_name", "").strip() if data.get("guest_name") else None
            session_id = data.get("session_id", "").strip() if data.get("session_id") else None

            if not user_message:
                return JsonResponse({"error": "Message is empty"})

            # Logged-in users
            if request.user.is_authenticated:
                 session_id = session_id or str(uuid4())  # Ensure session_id exists
                 bot_reply = generate_gemini_response(user_message)
                 ChatRecord.objects.create(
                     user=request.user,
                     session_id=session_id,  # ✅ Add this
                     user_message=user_message,
                     bot_response=bot_reply
                )
                 return JsonResponse({"response": bot_reply})

            # Anonymous users
            if guest_name and session_id:
                bot_reply = generate_gemini_response(user_message)
                ChatRecord.objects.create(
                    guest_name=guest_name,
                    session_id=session_id,
                    user_message=user_message,
                    bot_response=bot_reply
                )
                return JsonResponse({"response": bot_reply})

            return JsonResponse({"error": "Please enter your name to continue."})

        except Exception as e:
            return JsonResponse({"error": f"Bot Error: {str(e)}"})

    return JsonResponse({"error": "Invalid request method"})













def admin_form_view(request):
    if request.method == 'POST':
        form = MentalHealthSurveyForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.symptoms = ", ".join(form.cleaned_data['symptoms'])  # convert list to string
            instance.save()
            return redirect('admin-form-results')  # redirect after submission
    else:
        form = MentalHealthSurveyForm()

    return render(request, 'survey_form.html', {'form': form})

def admin_form_results_view(request):
    submissions = MentalHealthSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'admin/form_results.html', {'submissions': submissions})



from adminpanel.models import GalleryItem, ChatRecord  # already imported

def home(request):
    videos = YouTubeVideo.objects.all().order_by('-added_on')
    gallery_items = GalleryItem.objects.all().order_by('-created_at')
    ckeditor_content = CKEditorContent.objects.first()

    return render(request, 'healthapp/home.html', {
        'youtube_videos': videos,
        'gallery_items': gallery_items,
        'ckeditor_content': ckeditor_content,
    })



from adminpanel.models import CKEditorContent


