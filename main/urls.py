from django.conf.urls import url

from main import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^detalle-curso/(?P<curso_id>\d+)/$', views.show_curso_detail, name='show_curso_detail'),
    url(r'^detalle-servicio/(?P<service_id>\d+)/$', views.show_service_detail, name='show_service_detail'),
    url(r'^detalle-curso-especializado/(?P<curso_id>\d+)/$', views.specific_detail, name='specific_detail'),
    url(r'^show-video/(?P<pk_curso>\d+)/$', views.show_video, name='show_video'),
    url(r'^todos-cursos/$', views.full_cursos, name='full_cursos'),
    url(r'^todas-capacitationes/$', views.full_capacitation, name='full_capacitation'),
    url(r'^todas-servicio/$', views.full_services, name='full_services'),
    url(r'^list-especific-courses/(?P<course_id>\d+)/$', views.list_specific_couses, name='list_specific_couses'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^instrucctions/$', views.instrucction_for_account, name='instrucction_for_account'),
    url(r'^waytopay/$', views.way_to_pay, name='way_to_pay'),


    url(r'^nosotros/$', views.nosotros, name='nosotros'),]