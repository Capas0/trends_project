from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=64, default='test', unique=True)
    script = models.FileField(upload_to='scripts')

    def __str__(self):
        return self.name

