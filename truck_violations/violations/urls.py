from django.urls import path
from . import views  # Εισαγωγή των views από την τρέχουσα εφαρμογή

urlpatterns = [
    path('', views.violator_view, name='violator_form'),  # Προσθήκη του URL για τη φόρμα
]