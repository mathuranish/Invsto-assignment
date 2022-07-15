from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("importfile/", views.import_csv, name="import_csv"),  # for uploading file
    path(
        "startimport/", views.importer, name="importer"
    ),  # for preinstalled downloaded file
]
