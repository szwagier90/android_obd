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

class Measurement(models.Model):
	record = models.ForeignKey(Record)
	timestamp = models.BigIntegerField()
	AccX = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	AccY = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	AccZ = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	speed = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	rotation = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	altitude = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
