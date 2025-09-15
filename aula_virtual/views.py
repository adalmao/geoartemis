import datetime

import unicodedata
from unidecode import unidecode
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Person
from django.conf import settings
from .models import Company, Format, Course, HistoryFormats, Accident, Package, \
    Package_Course, \
    Package_User_Course, EspecificCourse, Capacitacion, CapacitationDetail, Service, ServiceDetail
from .forms import CompanyForm, FormatForm, AccidentForm, EmployeeForm, CourseForm, ProductForm, \
    Package_User_CourseForm, EspecificCourseForm, CapacitationForm, CapacitationDetailForm, ServiceDetailForm, \
    ServiceForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import HttpResponse,JsonResponse
import json
from aula_virtual.functions import create_zoom_room
from datetime import datetime

@login_required
def generatezoomroom(request,course_pk):
    if request.POST:
        course=get_object_or_404(EspecificCourse,pk=course_pk)
        now=datetime.now()
        date_time=now.strftime("%Y-%m-%dT%H:%M:%SZ")
        r=create_zoom_room(course.name,date_time)
        if r:
            course.zoom=r
            course.save()
            return JsonResponse({'response':'success','created':r},status=201)
        return JsonResponse({'response':'Operacion no aceptada'},status=400)
    else:
        return JsonResponse({'response':'Operacion no aceptada'},status=400)
@login_required
def home(request):
    # if user is admin
    return render(request, 'aula_virtual/panel.html', locals())


# panel de oshas
@login_required
def config(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, 'main/configuration.html', locals())


@login_required
def panel(request):
    # company = get_object_or_404(Company, slug=company_slug)
    return render(request, 'aula_virtual/panel.html', locals())


# panel de ley de seguridad ambiental
@login_required
def company_list(request):
    # if user is admin
    companias = Company.objects.all()
    # else
    # companies = Company.objects.get(su empresa)
    companies = list()
    for c in companias:
        if not c.slug == 'jra':
            companies.append(c)
    return render(request, "main/company/list.html", locals())


@login_required
def company_edit(request, company_slug):
    title = _('edit company')
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        update_action = request.GET.get('update')
        if update_action == 'company':
            company_form = CompanyForm(request.POST, request.FILES, instance=company)
            employee_form = EmployeeForm(instance=company.user)
            if company_form.is_valid():
                company = company_form.save()
                return redirect(reverse('aula_virtual:company_list'))
        if update_action == 'contact':
            employee_form = EmployeeForm(request.POST, request.FILES, instance=company.user)
            company_form = CompanyForm(instance=company)
            if employee_form.is_valid():
                employee = employee_form.save()
                return redirect(reverse('aula_virtual:company_list'))
    else:
        company_form = CompanyForm(instance=company)
        employee_form = EmployeeForm(instance=company.user)

    return render(request, "main/company/edit.html", locals())


@login_required
def show_file(request, requirement_pk, format_pk):
    show_archive = False
    format = Format.objects.get(pk=format_pk)
    if format.type_format == Format.ARCHIVO:
        show_archive = True
    return render(request, 'aula_virtual/requirements/formats/show_file_format.html', locals())


@login_required
def format_list(request, requirement_pk):
    # company = get_object_or_404(Company, slug=company_slug)
    course = EspecificCourse.objects.get(pk=requirement_pk)
    email=settings.ZOOM_USERID
    password=settings.ZOOM_PASSWORD
    show_courses = True
    if not request.user.is_superuser:
        try:
            package_User = Package_User_Course.objects.get(requirement=course, user=request.user)
            if not package_User.is_active:
                show_courses = False
                show_button = False
                message_buy = 'Su paquete sera activado en la proximas 24 hrs. Caso contrario omuniquese con el administrador para que active su paquete'

        except Package_User_Course.DoesNotExist:
            message_buy = 'Usted tiene que comprar un paquete para ingresar a la informacion del curso'
            show_courses = False
            show_button = True
    requirement = EspecificCourse.objects.get(pk=requirement_pk)
    title = requirement.name
    formats = Format.objects.filter(requirement=requirement)
    formats_pdf = list()
    formats_xlsx = list()
    if formats.count() != 0:
        for format in formats:
            if format.type_format == Format.ARCHIVO:
                formats_pdf.append(format)
            else:
                formats_xlsx.append(format)
            format.form = FormatForm(instance=format)
            format.history = HistoryFormats.objects.filter(format=format)
    else:
        message = ' Usted no tiene ARCHIVOS'
    return render(request, "aula_virtual/requirements/formats/list.html", locals())


@login_required
def format_update(request, requirement_pk, format_pk):
    requirement = get_object_or_404(EspecificCourse, pk=requirement_pk)
    format = get_object_or_404(Format, pk=format_pk)
    title = u'Requirement : {0} , updating format {1}'.format(requirement.name, format.name)

    if request.POST:
        form = FormatForm(request.POST, request.FILES, instance=format)
        if form.is_valid():
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.file.name = unidecode(history.file.name)
            history.save()
            format_new = form.save(commit=False)
            format_new.file.name = unidecode(format_new.file.name)
            format_new.save()

            return redirect(
                reverse('aula_virtual:format_list',
                        kwargs={"requirement_pk": requirement_pk}))
    else:
        form = FormatForm(instance=format)
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def specific_course_list(request, course_id):
    course = Course.objects.get(pk=course_id)
    courses_especific = EspecificCourse.objects.filter(course=course)
    title = 'Cursos especializados de ' + course.name
    return render(request, "aula_virtual/requirements/especific_courses_list.html", locals())


@login_required
def capacitacion_list(request):
    capacitacions = Capacitacion.objects.all()
    return render(request, "aula_virtual/capacitation/list.html", locals())


@login_required
def services_list(request):
    services = Service.objects.all()
    return render(request, "aula_virtual/services/list.html", locals())


@login_required
def requirements_list(request):
    # company = get_object_or_404(Company, slug=company_slug)

    requirements = Course.objects.all()

    return render(request, "aula_virtual/requirements/list.html", locals())


@login_required
def calendar_service(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/calendars/service.html", locals())


@login_required
def calendar_training(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/calendars/trainings.html", locals())


@login_required
def config_requirement_format_list(request, requirement_pk):
    requirement = Course.objects.get(pk=requirement_pk)
    title = _('requirement') + ' : ' + requirement.name
    formats = Format.objects.filter(requirement=requirement, company=None)
    formats_pdf = list()
    formats_xlsx = list()
    if formats.count() > 0:
        for format in formats:
            if format.type_format == Format.PLANES:
                formats_pdf.append(format)
            else:
                formats_xlsx.append(format)
            format.form = FormatForm(instance=format)
            format.history = HistoryFormats.objects.filter(format=format)
    else:
        message = ' Usted no tiene formatos'
    return render(request, "main/config/requirements/formats/list.html", locals())


@login_required
def config_requirement_format_update(request, requirement_pk, format_pk):
    requirement = get_object_or_404(Course, pk=requirement_pk)
    format = get_object_or_404(Format, pk=format_pk)
    title = 'Requirement : {0} , updating format {1}'.format(requirement.name, format.name)

    if request.POST:
        form = FormatForm(request.POST, request.FILES, instance=format)
        if form.is_valid():
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.save()

            form.save()

            return redirect(
                reverse('aula_virtual:config_requirement_format_list', kwargs={"requirement_pk": requirement_pk}))
    else:
        form = FormatForm(instance=format)
    return render(request, 'main/layout_with_out_nav_form.html', locals())


def mensual_report(request):
    return render(request, 'aula_virtual/reports/reports_mensual.html', locals())


@login_required
def config_requirement_format_new(request, requirement_pk):
    requirement = Course.objects.get(pk=requirement_pk)
    title = request.GET.get('title', '')
    title = '<b>Nuevo Formato</b> de {1} ,<br>para el requerimiento {0}'.format(requirement.name, title)

    if request.POST:
        form = FormatForm(request.POST, request.FILES)
        if form.is_valid():
            format = form.save(commit=False)
            format.requirement = requirement
            format.save()
        return redirect(
            reverse('aula_virtual:config_requirement_format_list', kwargs={"requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
    return render(request, 'main/layout_with_out_nav_form.html', locals())


@login_required
def edit_package(request, requirement_pk):
    course = EspecificCourse.objects.get(pk=requirement_pk)
    packages = Package.objects.all()
    try:
        package_course = Package_Course.objects.get(requirement=course)
        title = 'Selecciona nuevo paquete para el curso'
        if request.POST:
            package_course.package = Package.objects.get(pk=request.POST['packege_requirement'])
            package_course.save()
            return redirect(reverse('aula_virtual:requirements_list'))
        else:
            return render(request, 'aula_virtual/Products/edit_package_asociation.html', locals())
    except Package_Course.DoesNotExist:
        return redirect(reverse('aula_virtual:requirements_list'))


@login_required
def add_packege(request, requirement_pk):
    packages = Package.objects.all()
    course = EspecificCourse.objects.get(pk=requirement_pk)
    title = 'Paquetes - Requerimientos <br><h3>' + course.name + '</h3>'
    try:
        package_course = Package_Course.objects.get(requirement=course)
    except Package_Course.DoesNotExist:
        package_exist = False
        package_course = None
    if package_course:
        message = 'Ya existe un paquete asociado a este curso'
        package_exist = True
    else:
        if request.POST:
            package = Package.objects.get(pk=request.POST['packege_requirement'])
            package_course = Package_Course(requirement=course, package=package)
            package_course.save()
            return redirect(reverse('aula_virtual:requirements_list'))

    return render(request, 'aula_virtual/Products/package_asociation.html', locals())


@login_required
def specific_course_delete(request, course_especific_id):
    course = EspecificCourse.objects.get(pk=course_especific_id)
    course.delete()
    return redirect(reverse('aula_virtual:specific_course_list', kwargs={'course_id': course.course.pk}))


@login_required
def specific_course_new(request, course_id):
    course = Course.objects.get(pk=course_id)
    title = 'Nuevo Curso Especializado ' + course.name
    if request.POST:
        form = EspecificCourseForm(request.POST, request.FILES)
        if form.is_valid():
            courseEsp = form.save(commit=False)
            courseEsp.course = course
            courseEsp.save()
            return redirect(reverse('aula_virtual:specific_course_list', kwargs={'course_id': course.pk}))
        else:
            message = 'Revisa la informacion'
    else:
        message = 'Por defecto el curso sera gratuito, edite el paquete asociado despues de guardarlo...'
        form = EspecificCourseForm()
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def capacitacion_details_list(request, capacitation_id):
    capacitation = Capacitacion.objects.get(pk=capacitation_id)
    title = 'Detalles de capacitacion ' + capacitation.name
    capacitation_details = CapacitationDetail.objects.filter(capacitacion=capacitation)
    if request.POST:
        form = CapacitationDetailForm(request.POST)
        if form.is_valid():
            capacitationDetail = form.save(commit=False)
            capacitationDetail.capacitacion = capacitation
            capacitationDetail.save()
            return redirect(
                reverse('aula_virtual:capacitacion_details_list', kwargs={'capacitation_id': capacitation_id}))
        else:
            message = 'Revise la infromacion'
    else:
        form = CapacitationDetailForm()
    return render(request, 'aula_virtual/capacitation/details_list.html', locals())


@login_required
def services_details_list(request, services_id):
    service = Service.objects.get(pk=services_id)
    title = 'Detalles de servicio ' + service.name
    services_details = ServiceDetail.objects.filter(service=service)
    if request.POST:
        form = ServiceDetailForm(request.POST)
        if form.is_valid():
            serviceDetail = form.save(commit=False)
            serviceDetail.service = service
            serviceDetail.save()
            return redirect(
                reverse('aula_virtual:services_details_list', kwargs={'services_id': services_id}))
        else:
            message = 'Revise la infromacion'
    else:
        form = ServiceDetailForm()
    return render(request, 'aula_virtual/services/details_list.html', locals())


@login_required
def capacitation_detail_delete(request, capacitation_id):
    capacitation_detail = CapacitationDetail.objects.get(pk=capacitation_id)
    capacitation = capacitation_detail.capacitacion
    capacitation_detail.delete()
    return redirect(reverse('aula_virtual:capacitacion_details_list', kwargs={'capacitation_id': capacitation.pk}))


@login_required
def services_detail_delete(request, services_id):
    service_detail = ServiceDetail.objects.get(pk=services_id)
    service = service_detail.service

    service_detail.delete()
    return redirect(reverse('aula_virtual:services_details_list', kwargs={'services_id': service.pk}))


@login_required
def capacitation_delete(request, capacitation_id):
    capacitation = Capacitacion.objects.get(pk=capacitation_id)
    capacitation.delete()
    return redirect(reverse('aula_virtual:capacitacion_list'))


@login_required
def services_delete(request, services_id):
    service = Service.objects.get(pk=services_id)
    service.delete()
    return redirect(reverse('aula_virtual:services_list'))


@login_required
def capacitation_edit(request, capacitation_id):
    capacitation = Capacitacion.objects.get(pk=capacitation_id)
    title = 'Editar Capacitacion'
    if request.POST:
        form = CapacitationForm(request.POST, request.FILES, instance=capacitation)
        if form.is_valid():
            return redirect(reverse('aula_virtual:capacitacion_list'))
        else:
            message = 'Revise la informacion'
    else:
        form = CapacitationForm(instance=capacitation)
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def services_edit(request, services_id):
    service = Service.objects.get(pk=services_id)
    title = 'Editar Servicio'
    if request.POST:
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            return redirect(reverse('aula_virtual:services_list'))
        else:
            message = 'Revise la informacion'
    else:
        form = ServiceForm(instance=service)
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def capacitation_new(request):
    title = 'Nueva Capacitacion'
    if request.POST:
        form = CapacitationForm(request.POST, request.FILES)
        if form.is_valid():
            capacitation = form.save()
            return redirect(
                reverse('aula_virtual:capacitacion_details_list', kwargs={'capacitation_id': capacitation.pk}))
        else:
            message = 'Revise la informacion'
    else:
        form = CapacitationForm()
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def services_new(request):
    title = 'Nuevo Servicio'
    if request.POST:
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            return redirect(
                reverse('aula_virtual:services_details_list', kwargs={'services_id': service.pk}))
        else:
            message = 'Revise la informacion'
    else:
        form = ServiceForm()
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def requirement_new(request):
    # company = get_object_or_404(Company, slug=company_slug)
    title = 'Nuevo Curso'
    if request.POST:
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            requirement = form.save()
            # cr = Company_Requirement(company=company, requirement=requirement)
            # cr.save()

            return redirect(reverse('aula_virtual:specific_course_list', kwargs={'course_id': requirement.pk}))
        else:
            message = 'Revise la informacion'
    else:
        form = CourseForm()
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def config_requirement_new(request):
    global_config = True
    if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            requirement = form.save()
            requirement.save()
            return redirect(reverse('aula_virtual:config_requirements_list'))
    else:
        requirement_form = CourseForm()
    return render(request, 'main/config/requirements/new.html', locals())


@login_required
def product_list(request):
    packages = Package.objects.all()
    return render(request, "aula_virtual/Products/list.html", locals())


@login_required
def accident_list(request):
    # company = get_object_or_404(Company, slug=company_slug)
    # accidents = Accident.objects.filter(company=company)
    return render(request, "aula_virtual/accidents/list.html", locals())


@login_required
def format_new_other(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = '<b>{0}:</b> Nuevo formato de Registros y Evidencias'.format(requirement.name)

    if request.POST:
        format = Format(company=company, requirement=requirement, file=request.FILES['file'])
        format.type_format = Format.REGISTERS
        format.save()
        return redirect(
            reverse('aula_virtual:format_list',
                    kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
        return render(request, 'main/layout_form.html', locals())


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


@login_required
def format_new(request, requirement_pk):
    # company = get_object_or_404(Company, slug=company_slug)
    requirement = get_object_or_404(EspecificCourse, pk=requirement_pk)
    title = request.GET.get('title', '')
    title = u'<b>Nuevo Archivo</b> de {1} ,<br>para el curso {0}'.format(requirement.name, title)

    if request.POST:
        form = FormatForm(request.POST, request.FILES)
        if form.is_valid():
            format = form.save(commit=False)
            format.requirement = requirement
            format.file.name = unidecode(format.file.name)
            # format.company = company
            format.save()
        return redirect(
            reverse('aula_virtual:format_list', kwargs={"requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def buy_package(request, course_pk):
    course = EspecificCourse.objects.get(pk=course_pk)
    title = 'Compre Paquete ' + course.name
    package_buy_allow = True
    try:
        packages = Package_Course.objects.filter(Q(requirement=course), Q(is_active=True))
        if packages.count() <= 0:
            package_buy_allow = False
            message = 'No existe paquetes asociados por el momento'
        else:
            if request.POST:
                form = Package_User_CourseForm(request.POST, request.FILES)
                if form.is_valid():
                    form.instance.user = request.user
                    form.instance.requirement = course
                    package_user_buy = form.save()
                    return redirect(reverse('aula_virtual:format_list', kwargs={"requirement_pk": course.pk}))
                else:
                    message_error = 'Revise la informacion'
            else:
                form = Package_User_CourseForm()
    except Package_Course.DoesNotExist:
        package_buy_allow = False
        message = 'No existe paquetes asociados por el momento'
    if packages.count() <= 0:
        package_buy_allow = False
        message = 'No existe paquetes asociados por el momento'
    if request.POST:
        form = Package_User_CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.requirement = course
            package_user_buy = form.save()
            return redirect(reverse('aula_virtual:format_list', kwargs={"requirement_pk": course.pk}))
        else:
            message_error = 'Revise la informacion'
    else:
        form = Package_User_CourseForm()
    return render(request, 'aula_virtual/Products/buy_package.html', locals())


@login_required
def course_especific_edit(request, course_especific_id):
    course = EspecificCourse.objects.get(pk=course_especific_id)
    title = 'Editar Curso Especializado'
    if request.POST:
        form = EspecificCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect(reverse('aula_virtual:specific_course_list', kwargs={'course_id': course.course.pk}))
    else:
        form = EspecificCourseForm(instance=course)
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def requirement_edit(request, requirement_pk):
    course = Course.objects.get(pk=requirement_pk)
    title = 'Editar Curso'
    if request.POST:
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect(reverse('aula_virtual:requirements_list'))
    else:
        form = CourseForm(instance=course)
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def product_edit(request, product_pk):
    package = Package.objects.get(pk=product_pk)
    title = 'Editar Producto'
    if request.POST:
        form = ProductForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect(reverse('aula_virtual:product_list'))
        else:
            message = "Revisa la informacion ..."
    else:
        form = ProductForm(instance=package)
    return render(request, 'aula_virtual/layout_form.html', locals())


@login_required
def accident_edit(request, company_slug, accident_pk):
    company = get_object_or_404(Company, slug=company_slug)
    accident = Accident.objects.get(pk=accident_pk)
    title = 'editar accidente'
    if request.POST:
        form = AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            accident.title = form.instance.title
            accident.content = form.instance.content
            accident.type_accident = form.instance.type_accident
            accident.date = form.instance.date
            accident.evidence = form.files['evidence']
            accident.save()
            return redirect(reverse('aula_virtual:accident_list', kwargs={"company_slug": accident.company.pk}))
        return redirect(reverse('aula_virtual:accident_list', kwargs={"company_slug": accident.company.pk}))
    form = AccidentForm(instance=accident)

    return render(request, "main/accidents/accidents.html", locals())


@login_required
def requirement_delete(request, requirement_pk):
    course = Course.objects.get(pk=requirement_pk)
    if not course is None:
        course.delete()
        return redirect(reverse('aula_virtual:requirements_list'))
    else:
        return redirect(reverse('aula_virtual:requirements_list'))


@login_required
def product_delete(request, product_pk):
    package = Package.objects.get(pk=product_pk)
    if not package is None:
        package.delete()
        return redirect(reverse('aula_virtual:product_list'))
    else:
        return redirect(reverse('aula_virtual:product_list'))


@login_required
def accident_delete(request, company_slug, accident_pk):
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        return render(request, "main/accidents/list.html", locals())

    accident = Accident.objects.get(pk=accident_pk)
    if not accident is None:
        accident.delete()
        return redirect(reverse('aula_virtual:accident_list', kwargs={"company_slug": accident.company.slug}))
    else:
        message = 'ERROR: Bad Request ... !'
        return redirect(reverse('aula_virtual:accident_list', kwargs={"company_slug": accident.company.slug}))


@login_required
def product_new(request):
    title = 'Nuevo Paquete'
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect(reverse('aula_virtual:product_list'))
        else:
            message = 'Review all information ....'
    else:
        form = ProductForm
    return render(request, "aula_virtual/layout_form.html", locals())


@login_required
def accident_new(request):
    # company = get_object_or_404(Company, slug=company_slug)
    # title = 'nuevo accidente'
    # active_item_menu = 'accidents'
    # if request.POST:
    #     form = AccidentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         accident = form.save(commit=False)
    #         accident.company = company
    #         accident.save()
    #         return redirect(reverse('aula_virtual:accident_list', kwargs={"company_slug": company.slug}))
    #     else:
    #         message = 'Review all information . . .'
    # else:
    #     form = AccidentForm()
    return render(request, "aula_virtual/accidents/accidents.html", locals())


@login_required
def agreement(request):
    # company = get_object_or_404(Company, slug=company_slug)
    return render(request, "panel/agreement.html", locals())


@login_required
def reports(request):
    return render(request, "aula_virtual/reports/reports.html", locals())


@login_required
def active_package(request, pk_package):
    package = Package_User_Course.objects.get(pk=pk_package)
    if package.is_active:
        package.is_active = False
        package.save()
    else:
        package.is_active = True
        package.save()
    return redirect(reverse('aula_virtual:users'))


@login_required
def users(request):
    persons = Person.objects.all()
    users = list()
    for person in persons:
        person_dict = dict()
        person_dict['person'] = person
        person_dict['package'] = Package_User_Course.objects.filter(user=person)
        users.append(person_dict)

    return render(request, "aula_virtual/reports/users.html", locals())
