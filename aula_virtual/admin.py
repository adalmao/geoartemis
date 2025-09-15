from django.contrib import admin

from .models import Format, Report, Task, Accident, Meeting, HistoryFormats, Company, Course, Employee, EspecificCourse


class FormatAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'company','type_format')


admin.site.register(Employee)
admin.site.register(Course)
admin.site.register(EspecificCourse)
admin.site.register(Format)
admin.site.register(Report)
admin.site.register(Task)
admin.site.register(Accident)
admin.site.register(Meeting)
admin.site.register(HistoryFormats)
admin.site.register(Company)
