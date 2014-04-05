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

	def __unicode__(self):
		return "%s: %s (%s)" % (self.user, self.tags.all(), self.video_link)

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