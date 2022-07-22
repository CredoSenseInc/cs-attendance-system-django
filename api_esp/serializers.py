from rest_framework import serializers
# from .models import *
from device.models import commands, deviceInfo
from attendance.models import attendanceLog
from datetime import date
from django.db.models import Q

from employee.models import employee

# PLEASE CHECK CS_MANAGEMENT CODE FOR THIS SECTION. BOTH ARE SAME
class commands_serializer(serializers.ModelSerializer):
    class Meta:
        model = commands
        fields = '__all__'
    def validate(self, data):   
        if("attendance" in data['message']):
            try:
                todays_date = date.today()
                message_from_esp = str(data['message']).split(":")
                f_id = message_from_esp[1]
                
                daily_log_list = attendanceLog.objects.get(Q(emp__emp_finger_id_1 = f_id) | Q(emp__emp_finger_id_2 = f_id) | Q(emp__emp_finger_id_3 = f_id) | Q(emp__emp_finger_id_4 = f_id) | Q(emp__rfid_tag_number = f_id), date=todays_date)
                # print(data['scan_time'].time())
                if data['scan_time'].date() == todays_date:
                    if daily_log_list.emp_in_time is None:
                        # FOR CREDOSENSE ONLY REMOVE FOR SAUDA FASHION
                        if data['scan_time'].time().hour >= 13:
                            pass
                        else:
                            daily_log_list.emp_present = True
                            if(daily_log_list.date == data['scan_time'].date()):
                                daily_log_list.emp_in_time = data['scan_time'].time()
                    
                    elif daily_log_list.emp_in_time is not None:
                        if(daily_log_list.date == data['scan_time'].date()):
                            daily_log_list.emp_out_time = data['scan_time'].time()

                    daily_log_list.save()
                    data['isExecuted'] = True
                    # data['server_message'] = daily_log_list.emp.emp_id
                    data['server_message'] = str(daily_log_list.emp.emp_name) + " (" + str(daily_log_list.emp.emp_id) + ")"

                else:
                    data['server_message'] = "Wrong datetime."

            except Exception as e:
                print("Exception from commands_serializer:", e)

        elif("db_all" in data['message']):
            try:
                data['isExecuted'] = True
                emp_info = employee.objects.all()
                data['server_message'] = "Sending all"
            except Exception as e:
                print("Exception from commands_serializer:", e)

        elif("info" in data['message']):
            try:
                message_from_esp = str(data['message']).split(":")
                f_id = message_from_esp[1]
                
                emp_info = employee.objects.get(Q(emp_finger_id_1 = f_id) | Q(emp_finger_id_2 = f_id) | Q(emp_finger_id_3 = f_id) | Q(emp_finger_id_4 = f_id))
                data['isExecuted'] = True
                text_to_send = str(emp_info.emp_id)
                data['server_message'] = text_to_send
            except Exception as e:
                print("Exception from commands_serializer:", e)

        elif("ver" in data['message']):
            try:
                data['isExecuted'] = True
                data['server_message'] = "Data Received"
                device = deviceInfo.objects.get(device_id = data['device_id'])
                device.firmware_version = str(data['message']).split(":")[1]
                device.save()
            except Exception as e:
                print("Exception from commands_serializer:", e)

        elif("delete" in data['message']):
            try:
                data['isExecuted'] = False
                data['server_message'] = "Data Received"
            except Exception as e:
                print("Exception from commands_serializer:", e)

        else:
            data['isExecuted'] = True
            data['server_message'] = "Data Received"
        return data

class commands_serializer_pull(serializers.ModelSerializer):
    class Meta:
        model = commands
        fields = '__all__'

class attendance_serializer(serializers.ModelSerializer):
    class Meta:
        model = attendanceLog
        fields = '__all__'

    # def validate(self, data):
    #     try:
    #         check_user = MyUser.objects.get(user_unique_id=data['user_id'])
    #         print(type(check_user))
    #         try:
    #             check_reader = user_logger_list.objects.get(user = check_user , data_logger_id = data['device_id'])
    #         except Exception as e:
    #             raise serializers.ValidationError({"detail": "input is not valid"})

    #     except Exception as e:
    #         raise serializers.ValidationError({"detail": "input is not valid"})
            
    #     return data