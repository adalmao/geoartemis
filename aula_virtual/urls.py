from django.conf.urls import url
from django.views.static import serve

from aula_virtual import views
from django.conf import settings
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^generate/zoomroom/(?P<course_pk>\d+)/$', views.generatezoomroom, name='generatezoomroom'),

    #    url(r'^config/requirement-list/$', views.config_requirements_list, name='config_requirements_list'),
    url(r'^config/requirement-new/$', views.config_requirement_new, name='config_requirement_new'),

    url(r'^config/requirement/(?P<requirement_pk>\d+)/formats/$', views.config_requirement_format_list,
        name='config_requirement_format_list'),
    url(r'^config/requirement/(?P<requirement_pk>\d+)/format/new/$', views.config_requirement_format_new,
        name='config_requirement_format_new'),
    url(r'^config/requirement/(?P<requirement_pk>\d+)/format/(?P<format_pk>\d+)/update/$',
        views.config_requirement_format_update, name='config_requirement_format_update'),

    #    url(r'^company-new/$', views.company_new, name='company_new'),
    url(r'^company-list/$', views.company_list, name='company_list'),
    url(r'^company-edit/(?P<company_slug>[-\w]+)/$', views.company_edit, name='company_edit'),

    url(r'^buy-package/(?P<course_pk>\d+)/$', views.buy_package, name='buy_package'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^courses/(?P<course_id>\d+)/especialization/list/$', views.specific_course_list, name='specific_course_list'),
    url(r'^courses/(?P<course_id>\d+)/especialization/new/$', views.specific_course_new, name='specific_course_new'),
    url(r'^courses/(?P<course_especific_id>\d+)/delete/$', views.specific_course_delete, name='specific_course_delete'),
    url(r'^courses-especialization/(?P<course_especific_id>\d+)/edit/$', views.course_especific_edit,
        name='course_especific_edit'),
    url(r'^capacitation/$', views.capacitacion_list, name='capacitacion_list'),
    url(r'^capacitation/(?P<capacitation_id>\d+)/details/$', views.capacitacion_details_list,
        name='capacitacion_details_list'),
    url(r'^capacitation/(?P<capacitation_id>\d+)/details/delete/$', views.capacitation_detail_delete,
        name='capacitation_detail_delete'),
    url(r'^capacitation/new/$', views.capacitation_new, name='capacitation_new'),
    url(r'^capacitation/edit/(?P<capacitation_id>\d+)/$', views.capacitation_edit, name='capacitation_edit'),
    url(r'^capacitation/delete/(?P<capacitation_id>\d+)/$', views.capacitation_delete, name='capacitation_delete'),

    url(r'^services/$', views.services_list, name='services_list'),
    url(r'^services/(?P<services_id>\d+)/details/$', views.services_details_list,
        name='services_details_list'),
    url(r'^services/(?P<services_id>\d+)/details/delete/$', views.services_detail_delete,
        name='services_detail_delete'),
    url(r'^services/new/$', views.services_new, name='services_new'),
    url(r'^services/edit/(?P<services_id>\d+)/$', views.services_edit, name='services_edit'),
    url(r'^services/delete/(?P<services_id>\d+)/$', views.services_delete, name='services_delete'),

    url(r'^courses/$', views.requirements_list, name='requirements_list'),
    url(r'^courses/new/$', views.requirement_new, name='requirement_new'),
    url(r'^courses/edit/(?P<requirement_pk>\d+)/$', views.requirement_edit, name='requirement_edit'),
    url(r'^courses/delete/(?P<requirement_pk>\d+)/$', views.requirement_delete, name='requirement_delete'),
    url(r'^requirements/add_packege/(?P<requirement_pk>\d+)/$', views.add_packege, name='add_packege'),
    url(r'^requirements/edit_packege/(?P<requirement_pk>\d+)/$', views.edit_package, name='edit_package'),

    url(r'^course/(?P<requirement_pk>\d+)/formats/$', views.format_list, name='format_list'),
    url(r'^course/(?P<requirement_pk>\d+)/formats/new/$', views.format_new, name='format_new'),
    url(r'^course/(?P<requirement_pk>\d+)/formats/(?P<format_pk>\d+)/update/',
        views.format_update, name='format_update'),
    url(r'^course/(?P<requirement_pk>\d+)/formats/(?P<format_pk>\d+)/show-file/$', views.show_file,
        name='show_file'),

    url(r'^(?P<company_slug>[-\w]+)/config/$', views.config, name='config'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^reports/mensual/$', views.mensual_report, name='mensual_report'),
    url(r'^reports/users/$', views.users, name='users'),
    url(r'^reports/users/active-package/(?P<pk_package>\d+)/$', views.active_package, name='active_package'),

    url(r'^products/list/$', views.product_list, name='product_list'),
    url(r'^products/new/$', views.product_new, name='product_new'),
    url(r'^products/edit/(?P<product_pk>\d+)/$', views.product_edit, name='product_edit'),
    url(r'^products/delete/(?P<product_pk>\d+)/$', views.product_delete, name='product_delete'),

    url(r'^accident-list/$', views.accident_list, name='accident_list'),
    url(r'^(?P<company_slug>[-\w]+)/accident-edit/(?P<accident_pk>\d+)/$', views.accident_edit, name='accident_edit'),
    url(r'^accident-new/$', views.accident_new, name='accident_new'),
    url(r'^(?P<company_slug>[-\w]+)/accident-delete/(?P<accident_pk>\d+)/$', views.accident_delete,
        name='accident_delete'),
    url(r'^(?P<company_slug>[-\w]+)/agreement/$', views.agreement, name='agreement'),

]
urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
