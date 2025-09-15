from fullcalendar import views

__author__ = 'jona'

from django.urls import re_path
app_name = 'fullcalendar'
urlpatterns = [
    re_path(r'^list/$', views.calendar_list, name="list"),
    re_path(r'^new/$', views.calendar_new, name="new"),
    re_path(r'^view/(?P<calendar_id>\d+)/$', views.view_calendar,name="view_calendar"),
    re_path(r'^events/(?P<calendar_id>\d+)/$', views.events_json, name="events_json"),
    re_path(r'^event/save/(?P<slug>[-\w]+)$', views.save_event, name="save_event"),
    re_path(r'^event/$', views.get_event, name="get_event"),
    re_path(r'^event/update/', views.update_event, name="update_event"),
    re_path(r'^settings/(?P<slug>[-\w]+)/$', views.settings_calendar, name="settings_calendar")
]
