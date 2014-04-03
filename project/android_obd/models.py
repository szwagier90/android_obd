from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.CharField(max_length=50)

class Record(models.Model):
	user = ForeignKey(User)
	video_link = models.URLField(max_length=200, blank=True)
	tags = models.ManyToManyField(Tag)

class MeasurementType(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

class Measurement(models.Model):
	record = models.ForeignKey(Record)
	measurement_type = models.ForeignKey(MeasurementType)
	timestamp = models.DateTimeField()
	value = models.BinaryField()