# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from aula_virtual.models import Course, Company, Format, EspecificCourse, Capacitacion, CapacitationDetail, \
    Package_Course, Service, ServiceDetail
from geoartemis.settings import STATUS
from main.models import Subscribe


def first(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/home.html', locals())


def specific_detail(request, curso_id):
    cursos = Course.objects.all()
    services = Service.objects.all()
    course_especific = EspecificCourse.objects.get(pk=curso_id)
    title = u'Curso de especialización en ' + course_especific.name + ' 100% On Line'
    try:
        package = Package_Course.objects.get(requirement=course_especific, is_active=True)
        title += ' - ' + str(package.package.price) + ' dolares'
    except Package_Course.DoesNotExist:
        pass
    except Package_Course.MultipleObjectsReturned:
        package = Package_Course.objects.filter(requirement=course_especific, is_active=True).first()
        title += ' - ' + package.package.price + ' dólares'
    return render(request, 'main/especific_detail.html', locals())


def full_cursos(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/full_cursos.html', locals())


def list_specific_couses(request, course_id):
    course = Course.objects.get(pk=course_id)
    cursos = Course.objects.all()
    services = Service.objects.all()
    especific_courses = EspecificCourse.objects.filter(course=course)
    return render(request, 'main/full_especific_cursos.html', locals())


def full_capacitation(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    capacitations = Capacitacion.objects.all()
    details = list()
    detalles = dict()
    for capacitation in capacitations:
        detalles['detalles'] = CapacitationDetail.objects.filter(capacitacion=capacitation)
        detalles['capacitacion'] = capacitation
        details.append(detalles)
        detalles = dict()
    return render(request, 'main/full_capacitations.html', locals())


def full_services(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    details = list()
    detalles = dict()
    for service in services:
        detalles['detalles'] = ServiceDetail.objects.filter(service=service)
        detalles['service'] = service
        details.append(detalles)
        detalles = dict()
    return render(request, 'main/full_services.html', locals())


def show_curso_detail(request, curso_id):
    cursos = Course.objects.all()
    services = Service.objects.all()
    curso = Course.objects.get(pk=curso_id)
    return render(request, 'main/curso_detail.html', locals())


def show_service_detail(request, service_id):
    cursos = Course.objects.all()
    services = Service.objects.all()
    service = Service.objects.get(pk=service_id)
    details = ServiceDetail.objects.filter(service=service)
    return render(request, 'main/service_detail.html', locals())


def way_to_pay(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/way_to_pay.html', locals())


def contact(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/contacto.html', locals())


def instrucction_for_account(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/instruction_for_account.html', locals())


def show_video(request, pk_curso):
    try:
        curso = EspecificCourse.objects.get(pk=pk_curso)
    except EspecificCourse.DoesNotExist:
        try:
            curso = Course.objects.get(pk=pk_curso)
        except Course.DoesNotExist:
            pass
    return render(request, 'main/video_show.html', locals())


def subscribe(request):
    if request.POST:
        email = str(request.POST['email'])
        name = str(request.POST['name'])
        subs = Subscribe(name=name, email=email)
        subs.save()
        return render(request, 'main/home.html', locals())


def home(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/home.html', locals())


def nosotros(request):
    cursos = Course.objects.all()
    services = Service.objects.all()
    return render(request, 'main/nosotros.html', locals())
