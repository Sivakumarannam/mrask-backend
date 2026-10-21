from django.urls import path

from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<slug:slug>/', views.ProjectDetail.as_view()),
    path('contact/', views.ContactCreate.as_view()),
    path('weather/', views.WeatherView.as_view()),
    path('rag/ask/', views.RAGAskView.as_view()),
]
