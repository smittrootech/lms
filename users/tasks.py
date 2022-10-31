from celery import shared_task

@shared_task(name = "abc")
def print_message(message, *args, **kwargs):
  print(f"Celery is working!! Message is {message}")