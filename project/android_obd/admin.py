from django.contrib import admin
from android_obd.models import Tag, Record, Measurement

admin.site.register(Tag)
admin.site.register(Record)
admin.site.register(Measurement)
