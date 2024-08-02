from django.urls import path
from . import views
urlpatterns = [
    path('', views.AdminView.as_view(), name='admin-custom'),
]