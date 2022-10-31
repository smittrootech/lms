import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject.settings")
app = Celery("MyProject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
app.conf.beat_schedule = {
    #Scheduler Name
    'print-message-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'abc',  
        # Schedule      
        'schedule': 10.0,
        # Function Arguments 
        'args': ("Hello",) 
    }
}