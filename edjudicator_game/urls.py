from django.urls import path
from .views import ListHighScoresView, CreateHighScoresView, HighScoresDetailView, LoginView, RegisterUsersView

urlpatterns = [
    path("highscores/", ListHighScoresView.as_view(), name="high-scores-all"),
    path("highscores/create/", CreateHighScoresView.as_view(), name="high-scores-create"),
    path("highscores/<int:pk>/", HighScoresDetailView.as_view(), name="high-scores-detail"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/register/", RegisterUsersView.as_view(), name="auth-register"),
]