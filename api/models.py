from django.db import models


class RequestModel(models.Model):
    url = models.TextField()
    interval = models.IntegerField()


class RequestModelResponse(models.Model):
    request_model = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
