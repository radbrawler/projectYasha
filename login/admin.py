from django.contrib import admin
from . import models
# Register your models here.

# admin.site.register(models.User)
admin.site.register(models.Student)
admin.site.register(models.Admin)
admin.site.register(models.Faculty)
admin.site.register(models.NotificationFaculty)
admin.site.register(models.Object)
# admin.site.register(models.Message)
admin.site.register(models.Request  )
