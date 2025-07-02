from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='client_signup'),
    path('login/', views.login_view, name='client_login'),
    path('logout/', views.logout_view, name='client_logout'),
    path('profile/', views.profile_view, name='client_profile'),

     path('support/', views.support_forum, name='support_forum'),
    path('support/post/<uuid:post_id>/', views.support_post_detail, name='support_post_detail'),
]
