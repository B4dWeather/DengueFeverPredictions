from django.contrib import admin

from .models import WeatherRecord, ResultRecord, TrainingOptions, TrainingRecord

admin.site.register(WeatherRecord)
admin.site.register(ResultRecord)
admin.site.register(TrainingOptions)
admin.site.register(TrainingRecord)