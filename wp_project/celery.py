import json
import os
import requests
import logging
from celery import Celery
from django.db import IntegrityError

from wp_project import settings
from wp_project.helpers import get_random_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wp_project.settings')

app = Celery('wp_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = settings.TIME_ZONE

"""
    ----CELERY----
    To run worker: celery -A wp_project worker -l info
    To run beat: celery -A wp_project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler 
    To clear pending tasks: celery -A wp_project purge
    
"""


@app.task()
def clear_periodic_tasks():
    """
        When restarting Celery, we should clear previous PeriodicTasks, because we will setup them again
    """
    logging.info('[*] Clearing previous periodic tasks...')
    from django_celery_beat.models import PeriodicTask
    PeriodicTask.objects.all().delete()
    logging.info('[-] Clearing completed.')


@app.task()
def save_response(request_id, time_elapsed, response_content=None):
    """
    Saves response from request

    :param request_id: RequestModel instance id
    :param time_elapsed: Duration of the response
    :param response_content: Response content
    """
    from api.models import RequestModelResponse
    try:
        RequestModelResponse.objects.create(request_model_id=request_id,
                                            response=response_content,
                                            duration=time_elapsed).save()
    except IntegrityError:
        logging.critical('[!] Cannot save response, probably RequestModel does not exist! ID: {}'.format(request_id))
        refresh_periodic_tasks.delay()


@app.task()
def fetch_url(request_id, url):
    """
    Fetches given url

    :param request_id: RequestModel instance id
    :param url: Url to be fetched
    """
    logging.warning('[*] Fetching url -> {}'.format(url))
    time_elapsed = settings.FETCH_TIMEOUT
    try:
        response = requests.get(url, timeout=settings.FETCH_TIMEOUT)
        time_elapsed = response.elapsed.total_seconds()
        logging.warning(
            '[-] response content -> {}, elapsed {}s'.format(response.text, response.elapsed.total_seconds()))
        save_response.s(request_id, time_elapsed, response.text).apply_async()
    except requests.exceptions.Timeout:
        logging.error('[!] timeout exceeded, elapsed {}s'.format(settings.FETCH_TIMEOUT))
        save_response.s(request_id, time_elapsed).apply_async()
    except requests.exceptions.ConnectionError:
        logging.error('[!] max retries exceeded')
        save_response.s(request_id, time_elapsed).apply_async()
    except:
        logging.critical('[!] unknown exception')
        save_response.s(request_id, time_elapsed).apply_async()


@app.task()
def refresh_periodic_tasks():
    """
    Refreshes periodic tasks, for example when we delete RequestModel instance while celery is running
    save_response catches IntegrityException and calls this method
    """
    logging.info('[*] refreshing...')

    from django_celery_beat.models import PeriodicTask
    from django_celery_beat.models import IntervalSchedule
    from api.models import RequestModel

    old_periodic_tasks_ids = []
    for task in PeriodicTask.objects.all():
        old_periodic_tasks_ids.append(task.id)

    queryset = RequestModel.objects.all()
    for req in queryset:
        logging.info('[*] creating new PeriodicTask...')
        interval, created = IntervalSchedule.objects.get_or_create(every=req.interval, period=IntervalSchedule.SECONDS)
        PeriodicTask.objects.create(interval=interval, name=get_random_string(), task='wp_project.celery.fetch_url',
                                    args=json.dumps([req.id, req.url]))

    logging.info('[-] refreshing periodic tasks completed...')
    logging.info('[*] deleting previous periodic tasks...')

    for task_id in old_periodic_tasks_ids:
        PeriodicTask.objects.filter(id=task_id).delete()

    logging.info('[-] deleting completed...')


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    logging.info('[*] Setting up periodic tasks...')

    clear_periodic_tasks.delay()

    from api.models import RequestModel
    queryset = RequestModel.objects.all()
    for req in queryset:
        sender.add_periodic_task(req.interval, fetch_url.s(req.id, req.url))
