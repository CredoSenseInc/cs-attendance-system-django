import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs_attendance_system.settings")
django.setup()

from dashboard.views import create_daily_log
# your imports, e.g. Django models
try:
    print("Executing..........")
    create_daily_log()
    print("Finished")
except Exception as e:
    print(e)
    
# source /home/credtcad/virtualenv/cscloud.credosense.com/3.8/bin/activate && cd /home/credtcad/cscloud.credosense.com && python cron_task_run.py