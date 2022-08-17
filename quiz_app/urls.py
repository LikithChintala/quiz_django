from django.urls import path

from . import views

from .views import SignUpView

app_name = 'quiz_app'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('logout/', views.user_logout, name='logout'),
    path('', views.HomeView, name='home'),
    path('quiz/', views.IndexView.as_view(), name='index'),
    path('results/', views.ResultsView.as_view(), name='results'),
    path('add_score/', views.add_score, name='add_score'),
]
