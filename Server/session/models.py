from django.db import models

from test.models import Test


class Session(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(default=None, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='sessions')
    uuid = models.UUIDField(null=True)


class Event(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='events')
    time = models.DateTimeField(auto_now_add=True)
    status = models.TextField()


class Param(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='params')
    key = models.TextField()
    value = models.TextField()
