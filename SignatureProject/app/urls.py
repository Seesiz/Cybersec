from django.urls import path
from . import views

urlpatterns = [
    path('sign/', views.sign_document_view, name='sign_document'),
    path('view_signature/<path:signature_file>/', views.view_signature, name='view_signature'),
    path('verify/', views.verify_signature_view, name='verify_signature'),
]
