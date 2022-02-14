from django.urls import path

from .views import (
    QuotationListCreateView,
    QuotationRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', QuotationListCreateView.as_view()),
    path('<int:pk>/',  QuotationRetrieveUpdateDestroyView.as_view()),
]