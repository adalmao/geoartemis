from django.contrib import admin

# Register your models here.
from fullcalendar.models import Events,Calendar,EventType

admin.site.register(Events)
admin.site.register(Calendar)
admin.site.register(EventType)
