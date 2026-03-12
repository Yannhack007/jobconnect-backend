from django.urls import path, include
from .views import CompanyListCreateView, CompanyDetailView

urlpatterns = [
    path('', CompanyListCreateView.as_view(), name='Company List Create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='Company Detail'),
]
