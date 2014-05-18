from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Record(models.Model):
	user = models.ForeignKey(User)
	video_link = models.URLField(max_length=200, blank=True)
	tags = models.ManyToManyField(Tag)
	distance = models.IntegerField(blank=True)
	fuel_consumption = models.IntegerField(blank=True)
	public = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s (%d km): %s link:(%s) fuel:%d" % (self.user, self.distance, self.tags.all(), self.video_link, self.fuel_consumption)

class MeasurementType(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __unicode__(self):
		return "%s: %s" % (self.name, self.description)

class Measurement(models.Model):
	record = models.ForeignKey(Record)
	measurement_type = models.ForeignKey(MeasurementType)
	timestamp = models.DateTimeField()
	value = models.BinaryField()

	def __unicode__(self):
		return "%s: %s" % (self.timestamp, self.measurement_type.name)