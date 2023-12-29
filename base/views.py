from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view


def home(request):
    return render(request, "home.html")


def room(request):
    return render(request, "room.html")


@api_view(["GET"])
def connect(request):
    return HttpResponse(status=status.HTTP_200_OK)
