from celery import Celery

app = Celery('your_project_name', broker='redis://redis:6379/0')

@app.task
def add(x, y):
    return x + y