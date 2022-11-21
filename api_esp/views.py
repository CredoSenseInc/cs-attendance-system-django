from functools import partial
from django.shortcuts import render
from api_esp.serializers import *
from device.models import commands
from attendance.models import attendanceLog
from finger_template.models import template_info as Item

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import datetime
from datetime import date
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework.views import APIView
import time
# Create your views here.

# PLEASE CHECK CS_MANAGEMENT CODE FOR THIS SECTION. BOTH ARE SAME
class showCommands(APIView): 
    permission_classes = (IsAuthenticated,)
    def get(self, request, device_id):
        print(device_id)
        five_minutes_ago = datetime.datetime.now()  + datetime.timedelta(minutes=-5)
        print(five_minutes_ago)
        commandsToSend = commands.objects.filter(Q(isExecuted = False, timestamp__gte=five_minutes_ago, device_id = device_id) | Q(isExecuted = False, message__contains = "delete", device_id = device_id) | Q(isExecuted = False, message__contains = "update", device_id = device_id))
        serialize = commands_serializer(commandsToSend, many = True)
        return Response(serialize.data)

    def post(self, request, device_id):
        serializer = commands_serializer(data=request.data, many = True)
        if serializer.is_valid():
            serializer.save()
            return_message = []
            for i in serializer.data:
                if i['message'] == "db_all":
                    emp_info = employee.objects.all()
                    for emp in emp_info:
                        if emp.emp_finger_id_1 != "":
                            return_message.append({"name": emp.emp_name+ " (" + str(emp.emp_id) + ")", "finger_id" : emp.emp_finger_id_1})
                        if emp.emp_finger_id_2 != "":
                            return_message.append({"name": emp.emp_name+ " (" + str(emp.emp_id) + ")", "finger_id" : emp.emp_finger_id_2})
                        if emp.emp_finger_id_3 != "":
                            return_message.append({"name": emp.emp_name+ " (" + str(emp.emp_id) + ")", "finger_id" : emp.emp_finger_id_3})
                        if emp.emp_finger_id_4 != "":
                            return_message.append({"name": emp.emp_name+ " (" + str(emp.emp_id) + ")", "finger_id" : emp.emp_finger_id_4})

                if "info" in i['message']:
                    try:
                        emp_info = employee.objects.get(emp_id = i["server_message"])
                        return_message.append({"name": emp_info.emp_name + " (" + str(emp_info.emp_id) + ")", "finger_id" : str(i['message']).split(":")[1] })
                    except:
                        return_message.append({"name": "Not Found", "finger_id" : "Not Founds"})

                else:
                    return_message.append({"message": i['server_message']})
            return Response(return_message, status=status.HTTP_201_CREATED)
            
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
            serializer = commands_serializer_pull(data_obj, data=data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return JsonResponse(serializer.data) 
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def template_sync(request):
    if request.data["command"] == "free_temp_id":
        
        # Fisrt make a list of used id
        used_id = [0] * 10000
        free_id = -1
            
        for i in Item.objects.filter(group_id=request.data["group_id"], company_name=request.data["company_name"]):
            used_id[i.temp_id] = 1

        for i in range(1, 10000):
            print(i)
            if used_id[i] == 0:
                print("free id found")
                free_id = i
                break
        
        if free_id != -1:
            item = Item(temp_id=free_id, group_id=request.data["group_id"], company_name=request.data["company_name"])
            item.save()
        
        return Response(free_id, status=status.HTTP_201_CREATED)

    elif request.data["command"] == "download_template":
        print("download temp")
        item = Item.objects.filter(temp_id = request.data["temp_id"], group_id=request.data["group_id"], company_name=request.data["company_name"]).first()
        try:
            return Response(item.temp, status=status.HTTP_201_CREATED)
        except:
            return Response(-1, status=status.HTTP_201_CREATED)


    elif request.data["command"] == "upload_template":
        item = Item.objects.filter(temp_id=request.data["temp_id"], group_id=request.data["group_id"], company_name=request.data["company_name"]).first()
        try:
            item.delete()
        except:
            return Response(-1, status=status.HTTP_201_CREATED)

        item = Item(temp_id=request.data["temp_id"], group_id=request.data["group_id"], company_name=request.data["company_name"], temp=request.data["temp"])
        try:
            item.save()
            return Response(1, status=status.HTTP_201_CREATED)
        except:
            return Response(-1, status=status.HTTP_201_CREATED)


    elif request.data["command"] == "list_of_temp":

        temp_list = []

        for i in Item.objects.filter(group_id=request.data["group_id"], company_name=request.data["company_name"]):
            if i.temp:
                temp_list.append(i.temp_id)
        temp_list.sort()
        return Response(temp_list, status=status.HTTP_201_CREATED)

    elif request.data["command"] == "list_of_rfid":
        temp_list = []

        for i in Item.objects.filter(group_id=request.data["group_id"], company_name=request.data["company_name"]):
            if i.temp:
                temp_list.append(i.temp_id)
        temp_list.sort()
        return Response(temp_list, status=status.HTTP_201_CREATED)
