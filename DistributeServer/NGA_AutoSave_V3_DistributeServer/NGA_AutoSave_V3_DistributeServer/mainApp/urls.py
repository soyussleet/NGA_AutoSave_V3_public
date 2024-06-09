
from django.urls import path
from django.urls import include, path 
from . import views

urlpatterns = [
    path("test", views.test),
    path("dbGetAll",views.dbGetAll,name="dbGetAll"),
    path("postStat",views.postStat,name="postStat"),
    path("getPostRecord",views.getPostRecord,name="getPostRecord"),
    #path('savedFile',include('savedFileServe.urls'),name="savedFile")
]