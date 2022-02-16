from django.db import models

class File(models.Model):
    csv_file = models.FileField()
    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'file'

class Data(models.Model):
    image_name = models.CharField(max_length=1000, null=True, blank=True)
    objects_detected = models.CharField(max_length=1000)
    timestamp = models.DateField()

    class Meta:
        db_table = 'data'
