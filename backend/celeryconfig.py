from celery.schedules import crontab

broker_url = "redis://localhost:6379/1"
result_backend = "redis://localhost:6379/2"
broker_connection_retry_on_startup = True
timezone = "Asia/Kolkata"

beat_schedule = {
    'generate-report-every-month': {
        'task': 'tasks.generate_and_send_report',
        'schedule': crontab(day_of_month='1', hour='0', minute='0'),
    },
}
