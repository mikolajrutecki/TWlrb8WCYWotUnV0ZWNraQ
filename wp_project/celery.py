import os
import urllib.request
from datetime import timedelta
from celery import Celery, task
from django.utils import timezone

from wp_project import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wp_project.settings')

app = Celery('wp_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = settings.TIME_ZONE


def fetch_url(url):
    return urllib.request.urlopen(url).read().decode("utf-8")


@task()
def task1():
    now = timezone.now()
    print('{}:{}:{}'.format(now.day, now.minute, now.second))
    from api.models import RequestModel, RequestModelResponse
    requests = RequestModel.objects.filter(next_run_at__hour=now.hour,
                                           next_run_at__minute=now.minute,
                                           next_run_at__second=now.second)
    for req in requests:
        req.last_run_at = now
        req.next_run_at = req.last_run_at + timedelta(seconds=req.interval)
        req.save()
        print('{} with interval: {}, next run at: {}'.format(req.url, req.interval, req.next_run_at))
        resp = RequestModelResponse.objects.create(request_model=req, response=fetch_url(req.url), duration=3.24)  # TODO
        resp.save()