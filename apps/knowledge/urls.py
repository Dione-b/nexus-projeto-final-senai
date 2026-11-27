"""URLs do app knowledge (base de conhecimento)."""

from django.urls import path

from . import views

app_name = "knowledge"

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("novo/", views.document_upload, name="document_upload"),
]
