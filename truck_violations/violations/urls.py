from django.urls import path
from .views import ViolationRecordView, CalculateDaysDifferenceView

urlpatterns = [
    path('', ViolationRecordView.as_view(), name='record_violation'),
    path('calculate-days-difference/', CalculateDaysDifferenceView.as_view(), name='calculate_days_difference'),
]