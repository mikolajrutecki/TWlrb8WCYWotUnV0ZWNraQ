from django.db import models


class Request(models.Model):
    url = models.TextField()
    interval = models.IntegerField()


class RequestResponse(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    response = models.TextField()
    duration = models.DecimalField(max_digits=5, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

