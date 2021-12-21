from django.shortcuts import render
from api_esp.serializers import *
from device.models import commands
from attendance.models import attendanceLog

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
from datetime import date

# Create your views here.

@api_view(["GET","POST"])
def showCommands(request):
    if request.method == "GET":
        commandsToSend = commands.objects.filter(isExecuted = False)
        serialize = commands_serializer(commandsToSend, many = True)
        return Response(serialize.data)

    elif request.method == 'POST':
        serializer = commands_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def commandsUpdate(request, id):
    try: 
        data_obj = commands.objects.get(id=id) 
        print(data_obj)
    except commands.DoesNotExist: 
        return JsonResponse({'message': 'The data_obj does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # if request.method == 'GET': 
    #     serializer = commands_serializer(data_obj) 
    #     return JsonResponse(serializer.data) 
 
    if request.method == 'PUT': 
        data = JSONParser().parse(request) 
        serializer = commands_serializer(data_obj, data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    # elif request.method == 'DELETE': 
    #     data_obj.delete() 
    #     return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
'''
@api_view(["GET","POST"])
def attendance_api(request):
    if request.method == "GET":
        commandsToSend = attendanceLog.objects.filter(date=date.today())
        serialize = attendance_serializer(commandsToSend, many = True)
        return Response(serialize.data)

    elif request.method == 'POST':
        serializer = attendance_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def attendance_api_update(request, id):
    try: 
        data_obj = attendanceLog.objects.get(id=id) 
        print(data_obj)
    except commands.DoesNotExist: 
        return JsonResponse({'message': 'The data_obj does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # if request.method == 'GET': 
    #     serializer = attendance_serializer(data_obj) 
    #     return JsonResponse(serializer.data) 
 
    if request.method == 'PUT': 
        data = JSONParser().parse(request) 
        serializer = attendance_serializer(data_obj, data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    # elif request.method == 'DELETE': 
    #     data_obj.delete() 
    #     return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
'''