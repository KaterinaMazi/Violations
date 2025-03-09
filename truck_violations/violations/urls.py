from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_violation, name='record_violation'),
    path('calculate-days-difference/', views.calculate_days_difference, name='calculate_days_difference'),
]