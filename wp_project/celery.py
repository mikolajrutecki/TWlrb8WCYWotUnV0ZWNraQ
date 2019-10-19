import os
import requests
import logging
from celery import Celery, group
from wp_project import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wp_project.settings')

app = Celery('wp_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = settings.TIME_ZONE

"""
    ----CELERY----
    To run worker: celery -A wp_project worker -l info
    To run beat: celery -A wp_project beat -l info
    
"""


@app.task()
def save_response(request_id, time_elapsed, response_content=None):
    from api.models import RequestModelResponse
    RequestModelResponse.objects.create(request_model_id=request_id,
                                        response=response_content,
                                        duration=time_elapsed).save()


@app.task()
def fetch_url(request_id, url):
    logging.warning('Fetching url -> {}'.format(url))
    time_elapsed = settings.FETCH_TIMEOUT
    try:
        response = requests.get(url, timeout=settings.FETCH_TIMEOUT)
        time_elapsed = response.elapsed.total_seconds()
        logging.warning(
            '    response content -> {}, elapsed {}s'.format(response.text, response.elapsed.total_seconds()))
        save_response.s(request_id, time_elapsed, response.text).apply_async()
    except requests.exceptions.Timeout:
        logging.error('    timeout exceeded, elapsed {}s'.format(settings.FETCH_TIMEOUT))
        save_response.s(request_id, time_elapsed).apply_async()
    except requests.exceptions.ConnectionError:
        logging.error('    max retries exceeded')
        save_response.s(request_id, time_elapsed).apply_async()
    except:
        logging.critical('    unknown exception')
        save_response.s(request_id, time_elapsed).apply_async()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from api.models import RequestModel
    for req in RequestModel.objects.all():
        sender.add_periodic_task(req.interval, fetch_url.s(req.id, req.url))
