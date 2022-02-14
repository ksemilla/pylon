from django.urls import path

from .views import (
    CustomerListCreateView,
    CustomerRetrieveUpdateDestroy,
    CustomerContactListCreateView,
    CustomerContactRetrieveUpdateDestroyView,
    CustomerAddressListCreateView,
    CustomerAddressRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', CustomerListCreateView.as_view()),
    path('<int:customer_id>/', CustomerRetrieveUpdateDestroy.as_view()),
    path('<int:customer_id>/contacts/', CustomerContactListCreateView.as_view()),
    path('<int:customer_id>/contacts/<int:contact_id>/', CustomerContactRetrieveUpdateDestroyView.as_view()),
    path('<int:customer_id>/addresses/', CustomerAddressListCreateView.as_view()),
    path('<int:customer_id>/addresses/<int:address_id>/', CustomerAddressRetrieveUpdateDestroyView.as_view()),
]