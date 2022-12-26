from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(),
         name='user_registration'),
]
