from django.urls import path
from userauths import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns =[
    #profile section
    path("profile/update", views.editProfile, name="editprofile"),
    # User Authentication
    path('sign-up/', views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html", redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="sign-out.html"), name='sign-out'), 

    
]