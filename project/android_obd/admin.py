from django.contrib import admin
from android_obd.models import Tag, Record, MeasurementType, Measurement

admin.site.register(Tag)
admin.site.register(Record)
admin.site.register(MeasurementType)
admin.site.register(Measurement)
