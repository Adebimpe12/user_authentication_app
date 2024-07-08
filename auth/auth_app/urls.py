from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView,  CustomTokenObtainPairView, AddUserToOrganisationView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),  # Example endpoint for registration
    path('login/', LoginView.as_view(), name='login'),           # Example endpoint for login
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('organisations/<int:id>/users/', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]
 
