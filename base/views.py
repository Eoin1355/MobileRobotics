from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["GET"])
def connect(request):
    return HttpResponse(status=status.HTTP_200_OK)
