from django.contrib import admin
from django.urls import include, path
from portfolio import views as portfolio_views

urlpatterns = [
    path('', portfolio_views.APIDocsView.as_view()),
    path('health/', portfolio_views.HealthCheckView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('portfolio.urls')),
]
