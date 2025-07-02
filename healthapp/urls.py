from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('survey_form/', views.mental_health_form, name='mental_health_form'),  # Mental health form
    path('relaxing_videos/', views.relaxing_videos, name='relaxing_videos'),
    path('articles/', views.articles, name='articles'),
    path('get-videos/', views.get_youtube_videos, name='get_youtube_videos'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    

    # Admin form panel
    path('admin-panel/forms/', views.admin_form_view, name='admin-form'),
    path('admin-panel/forms/results/', views.admin_form_results_view, name='admin-form-results'),
    

]
