from django.urls import path

from .views import (
    InventoryListCreateView,

    StockCreateAPIView,
    StockRetrieveUpdateDestroyView,
    StockInstanceListCreateView,
    StockInstanceRetrieveUpdateDestroyView,
    StockVendorListCreateView,
    StockVendorRetrieveUpdateDestroyView,

    LaborListCreateView,
    LaborRetrieveUpdateDestroyView,
    LaborVendorListCreateView,
    LaborVendorRetrieveUpdateDestroyView,

    DocumentListCreateView,
    DocumentRetrieveUpdateDestroyView,
    DocumentVendorListCreateView,
    DocumentVendorRetrieveUpdateDestroyView,

    AssemblyListCreateView,
    AssemblyRetrieveUpdateDestroyView,
    AssemblyInstanceListCreateView,
    AssemblyInstanceRetrieveUpdateDestroyView,
    AssemblyVendorListCreateView,
    AssemblyVendorRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', InventoryListCreateView.as_view()),

    path('stocks/', StockCreateAPIView.as_view()),
    path('stocks/<int:stock_id>/', StockRetrieveUpdateDestroyView.as_view()),
    path('stocks/<int:stock_id>/instances/', StockInstanceListCreateView.as_view()),
    path('stocks/<int:stock_id>/instances/<int:pk>/', StockInstanceRetrieveUpdateDestroyView.as_view()),
    path('stocks/<int:stock_id>/vendors/', StockVendorListCreateView.as_view()),
    path('stocks/<int:stock_id>/vendors/<int:pk>/', StockVendorRetrieveUpdateDestroyView.as_view()),

    path('labor/', LaborListCreateView.as_view()),
    path('labor/<int:labor_id>/', LaborRetrieveUpdateDestroyView.as_view()),
    path('labor/<int:labor_id>/vendors/', LaborVendorListCreateView.as_view()),
    path('labor/<int:labor_id>/vendors/<int:pk>/', LaborVendorRetrieveUpdateDestroyView.as_view()),

    path('document/', DocumentListCreateView.as_view()),
    path('document/<int:document_id>/', DocumentRetrieveUpdateDestroyView.as_view()),
    path('document/<int:document_id>/vendors/', DocumentVendorListCreateView.as_view()),
    path('document/<int:document_id>/vendors/<int:pk>/', DocumentVendorRetrieveUpdateDestroyView.as_view()),

    path('assembly/', AssemblyListCreateView.as_view()),
    path('assembly/<int:assembly_id>/', AssemblyRetrieveUpdateDestroyView.as_view()),
    path('assembly/<int:assembly_id>/instances/', AssemblyInstanceListCreateView.as_view()),
    path('assembly/<int:assembly_id>/instances/<int:pk>/', AssemblyInstanceRetrieveUpdateDestroyView.as_view()),
    path('assembly/<int:assembly_id>/vendors/', AssemblyVendorListCreateView.as_view()),
    path('assembly/<int:assembly_id>/vendors/<int:pk>/', AssemblyVendorRetrieveUpdateDestroyView.as_view()),
]