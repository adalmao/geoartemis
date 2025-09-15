from django.urls import  re_path

from main import views
app_name = 'main'
urlpatterns = [

    re_path(r'^$', views.home, name='home'),
    re_path(r'^subscribe/$', views.subscribe, name='subscribe'),
    re_path(r'^detalle-curso/(?P<curso_id>\d+)/$', views.show_curso_detail, name='show_curso_detail'),
    re_path(r'^detalle-servicio/(?P<service_id>\d+)/$', views.show_service_detail, name='show_service_detail'),
    re_path(r'^detalle-curso-especializado/(?P<curso_id>\d+)/$', views.specific_detail, name='specific_detail'),
    re_path(r'^show-video/(?P<pk_curso>\d+)/$', views.show_video, name='show_video'),
    re_path(r'^todos-cursos/$', views.full_cursos, name='full_cursos'),
    re_path(r'^todas-capacitationes/$', views.full_capacitation, name='full_capacitation'),
    re_path(r'^todas-servicio/$', views.full_services, name='full_services'),
    re_path(r'^list-especific-courses/(?P<course_id>\d+)/$', views.list_specific_couses, name='list_specific_couses'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^instrucctions/$', views.instrucction_for_account, name='instrucction_for_account'),
    re_path(r'^waytopay/$', views.way_to_pay, name='way_to_pay'),


    re_path(r'^nosotros/$', views.nosotros, name='nosotros'),]