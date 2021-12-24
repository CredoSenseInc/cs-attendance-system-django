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
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework.views import APIView
import time
# Create your views here.


class showCommands(APIView): 
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        five_minutes_ago = datetime.datetime.now()  + datetime.timedelta(minutes=-5)
        print(five_minutes_ago)
        commandsToSend = commands.objects.filter(Q(isExecuted = False, timestamp__gte=five_minutes_ago) | Q(isExecuted = False, message__contains = "delete"))
        serialize = commands_serializer(commandsToSend, many = True)
        return Response(serialize.data)

    def post(self, request):
        serializer = commands_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data["server_message"], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class commandsUpdate(APIView):
    permission_classes = (IsAuthenticated,) 
    def put(self, request, id):
        try: 
            data_obj = commands.objects.get(id=id) 
            print(data_obj)
        except commands.DoesNotExist: 
            return JsonResponse({'message': 'The data_obj does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    
        if request.method == 'PUT': 
            data = JSONParser().parse(request) 
            serializer = commands_serializer(data_obj, data=data) 
            if serializer.is_valid(): 
                serializer.save() 
                return JsonResponse(serializer.data) 
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)