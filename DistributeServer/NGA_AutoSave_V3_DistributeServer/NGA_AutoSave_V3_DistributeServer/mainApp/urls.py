
from django.urls import path

from . import views

urlpatterns = [
    path("test", views.test),
    path("dbGetAll",views.dbGetAll)
]