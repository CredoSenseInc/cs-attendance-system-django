from rest_framework import serializers
# from .models import *
from device.models import commands
from attendance.models import attendanceLog

class commands_serializer(serializers.ModelSerializer):
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