
from django.urls import path

from . import views

app_name = 'savedFile'

urlpatterns = [
    path("test", views.test),
    path("",views.saved_files_serve,name="savedFileRoot")
]