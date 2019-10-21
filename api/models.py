from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from wp_project.celery import refresh_periodic_tasks


class RequestModel(models.Model):
    url = models.TextField()
    interval = models.IntegerField()


@receiver(post_save, sender=RequestModel)
def save_report(**kwargs):
    """
    Post save signal which updates our Periodic Tasks while celery is running
    """
    refresh_periodic_tasks.delay()


class RequestModelResponse(models.Model):
    request_model = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
