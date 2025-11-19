from celery import shared_task

@shared_task
def send_test_email():
    print("Celery is working perfectly!")
    return "OK"
