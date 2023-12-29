from . import views
from django.urls import path

urlpatterns = [
    path("", views.connect),
    path("room/", views.room, name="room"),
]
