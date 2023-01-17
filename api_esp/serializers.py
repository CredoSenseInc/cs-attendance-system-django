from rest_framework import serializers
# from .models import *
from device.models import commands, deviceInfo
from attendance.models import attendanceLog
from datetime import date
from django.db.models import Q

from employee.models import employee

from settings.models import *
from datetime import date
import datetime

# PLEASE CHECK CS_MANAGEMENT CODE FOR THIS SECTION. BOTH ARE SAME
class commands_serializer(serializers.ModelSerializer):
    class Meta:
        model = commands
        fields = '__all__'
    def validate(self, data):   
        if("attendance" in data['message']):
            try:
                # todays_date = date.today()
                todays_date = data['scan_time'].date()
                create_log_for_date(todays_date)
                message_from_esp = str(data['message']).split(":")
                f_id = message_from_esp[1]
                
                daily_log_list = attendanceLog.objects.get(Q(emp__emp_finger_id_1 = f_id) | Q(emp__emp_finger_id_2 = f_id) | Q(emp__emp_finger_id_3 = f_id) | Q(emp__emp_finger_id_4 = f_id) | Q(emp__rfid_tag_number = f_id), date=todays_date)
                # print(data['scan_time'].time())
                if data['scan_time'].date() == todays_date:
                    if daily_log_list.emp_in_time is None:
                        # # FOR CREDOSENSE ONLY REMOVE FOR SAUDA FASHION
                        # # if data['scan_time'].time().hour >= 13:
                        # if 0:
                        #     pass
                        # else:
                        daily_log_list.emp_present = True
                        if(daily_log_list.date == data['scan_time'].date()):
                            daily_log_list.emp_in_time = data['scan_time'].time()

                    elif daily_log_list.emp_in_time is not None:
                        if (daily_log_list.emp_in_time > data['scan_time'].time()):
                            daily_log_list.emp_in_time = data['scan_time'].time()
                        
                        elif daily_log_list.emp_out_time is None:
                            daily_log_list.emp_out_time = data['scan_time'].time()

                        elif (daily_log_list.emp_out_time < data['scan_time'].time()):
                                daily_log_list.emp_out_time = data['scan_time'].time()
                    else:
                        print("do you need this datetime ?? ")
                        print(data['scan_time'])

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
                
                emp_info = employee.objects.get(Q(emp_finger_id_1 = f_id) | Q(emp_finger_id_2 = f_id) | Q(emp_finger_id_3 = f_id) | Q(emp_finger_id_4 = f_id)| Q(rfid_tag_number = f_id) )
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

        elif("update" in data['message']):
            try:
                # device_id = data['device_id']
                data['isExecuted'] = False
                # message = data['message']
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


def create_log_for_date(todays_date = date.today()):
    print("Creating daily log")
    print(todays_date)
    print(datetime.datetime.now().strftime("%H:%M:%S"))
    all_emp = employee.objects.all()
    settings = settings_db.objects.last()   
    offDay = str(settings.offDay).split(",")
    workDay = str(settings.workDay).split(",")
    print(workDay)

    for i in range (len(offDay)):
        if(offDay[i]!=''):
            offDay[i] = datetime.datetime.strptime(offDay[i], '%m/%d/%Y').date()
        # offDay[i] = datetime.datetime.strptime(offDay[i], '%Y-%m-%d').date()
        # print(offDay[i])

    for i in range (len(workDay)):
        if(workDay[i]!=''):
            workDay[i] = datetime.datetime.strptime(workDay[i], '%m/%d/%Y').date()
        # workDay[i] = datetime.datetime.strptime(workDay[i], '%Y-%m-%d').date()
        # print(offDay[i])
    weekends = []

    if settings.week_saturday:
        weekends.append("Saturday")
    if settings.week_sunday:
        weekends.append("Sunday")
    if settings.week_monday:
        weekends.append("Monday")
    if settings.week_tuesday:
        weekends.append("Tuesday")
    if settings.week_wednesday:
        weekends.append("Wednesday")
    if settings.week_thursday:
        weekends.append("Thursday")
    if settings.week_friday:
        weekends.append("Friday")

    print(todays_date.strftime('%A'))
    print(weekends)

    if (todays_date.strftime('%A') in weekends):
        if(todays_date in workDay):
            all_emp = employee.objects.all()
            check_today_log = attendanceLog.objects.filter(date = todays_date).count()
            print(check_today_log)
            if (check_today_log == 0):
                for i in range (len(all_emp)):
                    attendance = attendanceLog()
                    attendance.emp = all_emp[i]
                    attendance.finger1 = all_emp[i]
                    attendance.date = todays_date
                    attendance.save()

    elif(todays_date in offDay):
        # weekend
        pass
    else:
        all_emp = employee.objects.all()
        check_today_log = attendanceLog.objects.filter(date = todays_date).count()
        print(check_today_log)
        if (check_today_log == 0):
            for i in range (len(all_emp)):
                attendance = attendanceLog()
                attendance.emp = all_emp[i]
                attendance.finger1 = all_emp[i]
                attendance.date = todays_date
                attendance.save()   

    if (todays_date.strftime('%A') in weekends or todays_date in offDay and todays_date not in workDay):
        print("Today is weekend")
    
    elif(todays_date.strftime('%A') not in weekends or todays_date not in offDay and todays_date  in workDay):
        print("Today is workday")
        all_emp = employee.objects.all()
        check_today_log = attendanceLog.objects.filter(date = todays_date).count()
        print(check_today_log)
        if (check_today_log == 0):
            for i in range (len(all_emp)):
                attendance = attendanceLog()
                attendance.emp = all_emp[i]
                attendance.finger = all_emp[i]
                attendance.date = todays_date
                attendance.save()
                
    # check_today_log = attendanceLog.objects.filter(date = todays_date).count()
    
    # if check_today_log > 0:
    #     show_table = True
    # else:
    #     show_table = False


    show_table = True
    if (todays_date.strftime('%A') in weekends):
        show_table = False
        if(todays_date in workDay):
            show_table = True
    elif(todays_date in offDay):
        show_table = False
    else:
        show_table = True
    return show_table