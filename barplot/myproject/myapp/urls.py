# myapp/urls.py
from django.urls import path
from .views import WordFrequencyChart

urlpatterns = [
    path('word-frequency-chart/', WordFrequencyChart.as_view(), name='word_frequency_chart'),
]
