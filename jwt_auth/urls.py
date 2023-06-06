from rest_framework.urls import path
# from views import RegisterView, LoginView, UserListView, UserDetailView
# from .views import RegisterView, LoginView, UserListView, UserDetailView
from jwt_auth.views import RegisterView, LoginView, UserListView, UserDetailView

urlpatterns = [
  path('register/', RegisterView.as_view()),
  path('login/', LoginView.as_view()),
  path('', UserListView.as_view()),
  path('<int:pk>/', UserDetailView.as_view())
]
