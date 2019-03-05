from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@csrf_exempt
@api_view(['POST'])
def get_changes(request):
    return Response(data = request.data)


@api_view(['GET'])
def get_changes_show(request):
    return Response(status=status.HTTP_404_NOT_FOUND, data={'msg': "This is made for post requests"})