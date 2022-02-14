from django.urls import path

from .views import (
    VendorListCreateView,
    VendorRetrieveUpdateDestroyView,
    VendorAddressCreateView,
    VendorAddressRetrieveUpdateDestroyView,
    VendorContactCreateView,
    VendorContactRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', VendorListCreateView.as_view()),
    path('<int:pk>/', VendorRetrieveUpdateDestroyView.as_view()),
    path('<int:vendor_id>/addresses/', VendorAddressCreateView.as_view()),
    path('<int:vendor_id>/addresses/<int:pk>/', VendorAddressRetrieveUpdateDestroyView.as_view()),
    path('<int:vendor_id>/contacts/', VendorContactCreateView.as_view()),
    path('<int:vendor_id>/contacts/<int:pk>/', VendorContactRetrieveUpdateDestroyView.as_view()),
]