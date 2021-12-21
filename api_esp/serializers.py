from rest_framework import serializers
# from .models import *
from device.models import commands
from attendance.models import attendanceLog
from datetime import date

class commands_serializer(serializers.ModelSerializer):
    class Meta:
        model = commands
        fields = '__all__'
    def validate(self, data):   
        if("attendance" in data['message']):
            try:
                todays_date = date.today()
                messange_from_esp = str(data['message']).split(":")
                f_id = messange_from_esp[1]
                daily_log_list = attendanceLog.objects.get(finger = f_id, date=todays_date)
                print(data['scan_time'].time())
                if daily_log_list.emp_in_time is None:
                    daily_log_list.emp_in_time = data['scan_time'].time()
                
                elif daily_log_list.emp_in_time is not None:
                    daily_log_list.emp_out_time = data['scan_time'].time()

                daily_log_list.save()
                data['isExecuted'] = True
            except Exception as e:
                print(e)
        return data

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