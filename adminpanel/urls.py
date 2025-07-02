from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.login_view, name='admin_login'),  

    path('signup/', views.signup_view, name='admin_signup'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('remove/<int:video_id>/', views.remove_video, name='remove_video'),
      path('forms/', views.admin_forms_view, name='admin_forms'),
      path('logout/', views.logout_view, name='admin_logout'),
       path('admin/chat-records/', views.chat_records_view, name='chat-records'),



    path('client-users/', views.client_users_list, name='client_users'),
    path('client-users/<int:user_id>/', views.client_user_detail, name='client_user_detail'),

     path('anonymous-sessions/', views.anonymous_sessions, name='anonymous_sessions'),
    path('anonymous-sessions/<uuid:session_id>/', views.anonymous_chat_detail, name='anonymous_chat_detail'),


    path('adminpanel/gallery/', views.gallery_upload_view, name='gallery_upload'),
      path('gallery/delete/<int:item_id>/', views.delete_gallery_item, name='delete_gallery_item'),

      path('adminpanel/ck-editor/', views.ck_editor_admin, name='ck_editor_admin'),

      path('support-forum/', views.support_admin_view, name='support_admin_view'),



    
]



    

