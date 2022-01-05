from dashboard.views import create_daily_log
# your imports, e.g. Django models

def my_scheduled_job():
    print("Daily Log Create Task")
    create_daily_log()