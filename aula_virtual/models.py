import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _


class Product(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)


def upload_image_to(instance, filename):
    filename = os.path.splitext(filename)
    filename = str(instance.ruc) + filename[1]
    return filename


class Company(models.Model):
    ruc = models.IntegerField(null=False, blank=False, unique=True)
    name = models.CharField(_('company name'), max_length=100, null=False, blank=False, unique=True)
    short_name = models.CharField(_('short name'), max_length=100, null=False, blank=False, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, blank=True, null=True, unique=True)
    logo = models.ImageField(_('logo'), upload_to=upload_image_to, blank=True, null=True)
    address = models.CharField(_('address'), max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(self.short_name)
        super(Company, self).save(**kwargs)


class Course(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    file = models.FileField(_('file'), upload_to="cursos/", null=True)
    video = models.CharField(_('video'),max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name


class Capacitacion(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    file = models.FileField(_('file'), upload_to="capacitationes/", null=True)


class Service(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    file = models.FileField(_('file'), upload_to="services/", null=True)


class ServiceDetail(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    descrip = models.CharField(max_length=250, null=False, blank=False)


class CapacitationDetail(models.Model):
    capacitacion = models.ForeignKey(Capacitacion,on_delete=models.CASCADE)
    descrip = models.CharField(max_length=250, null=False, blank=False)


class EspecificCourse(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)
    zoom = models.CharField(_('Zoom'),max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    file = models.FileField(_('file'), upload_to="cursosEspecificos/", null=True)
    video = models.FileField(_('video'), upload_to="cursosEspecificos/videos", null=True)
    start_date = models.DateTimeField(_('Fecha inicio'), null=False, default=datetime.now())
    duration = models.IntegerField(_('Duracion'), null=True, blank=True)
    benefits = models.CharField(_('Beneficios'), null=True, blank=True, max_length=100)
    certificate = models.CharField(_('Certificacion'), null=True, blank=True, max_length=100)
    introduction = models.TextField(_('Introduccion: '), null=True, blank=True)
    object = models.TextField(_('Objectivo: '), null=True, blank=True)
    go_to = models.TextField(_('Dirigido a: '), null=True, blank=True)
    temario = models.TextField(_('Temario: '), null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name


class Employee(User):
    code = models.CharField(max_length=50, null=False, blank=False)
    company = models.ForeignKey(Company, null=False, blank=False,on_delete=models.CASCADE)
    time = models.IntegerField(default=0)


Company.user = property(lambda e: Employee.objects.filter(company=e).first())


class Meeting(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100, null=True, blank=True)


def directiry_path(filename):
    path = os.path.dirname(__file__)
    return path + filename


class Evidence(models.Model):
    filename = models.CharField(max_length=50, null=False)
    file = models.FileField()


class Accident(models.Model):
    ACCIDENT = 1
    INCIDENT = 2
    TYPE_ACCIDENT_CHOICES = (
        (ACCIDENT, 'ACCIDENT'),
        (INCIDENT, 'INCIDENT')
    )
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    type_accident = models.IntegerField(_('type accident'), choices=TYPE_ACCIDENT_CHOICES, default=ACCIDENT)  # NOQA
    date = models.DateField(_('date'), null=False, default=datetime.now)
    company = models.ForeignKey(Company, null=False, blank=False,on_delete=models.CASCADE)
    evidence = models.FileField(_('evidence'), upload_to="accident/", null=True)


class Task(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField()
    company = models.ForeignKey(Company, null=False, blank=False,on_delete=models.CASCADE)
    type_calendar = models.IntegerField(null=False, blank=False)
    meeting = models.ForeignKey(Meeting, null=True, blank=True,on_delete=models.CASCADE)
    charge = models.CharField(max_length=100, null=False, blank=False)  # responsable
    content = models.TextField(null=False, blank=False)  # contenido
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # Falta anadir evidencia de tipo imagen
    # status = models.IntegerField("status", choises = STATUS, default = )
    expiration = models.DateTimeField()


class Report(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, null=False, blank=False,on_delete=models.CASCADE)


class Package(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    count_mounth = models.IntegerField(null=False)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.title + '-----$/.' + str(self.price)

    def __unicode__(self):
        return u'%s' % self.title + '-----$/.' + "{0:.2f}".format(self.price)


class Package_User_Course(models.Model):
    requirement = models.ForeignKey(EspecificCourse,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    date_buy = models.DateField(null=False, auto_now_add=True)
    date_activated = models.DateField(null=True)
    file = models.FileField(upload_to="payment", null=True, blank=True)
    is_active = models.BooleanField(null=False, default=False)


class Package_Course(models.Model):
    requirement = models.ForeignKey(EspecificCourse,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    is_active = models.BooleanField(null=False, default=True)


class Format(models.Model):
    VIDEOS = 1
    ARCHIVO = 2
    TYPE_FORMAT_CHOICES = (
        (VIDEOS, 'VIDEOS'),
        (ARCHIVO, 'ARCHIVO')
    )
    requirement = models.ForeignKey(EspecificCourse,on_delete=models.CASCADE)
    file = models.FileField(upload_to="formatos/", null=False, blank=False)
    type_format = models.IntegerField(choices=TYPE_FORMAT_CHOICES, default=ARCHIVO,
                                      null=True)  # is if format is planes or registros
    name = models.CharField(_('name'), max_length=100, null=False, blank=False)


class HistoryFormats(models.Model):
    format = models.ForeignKey(Format, null=True, blank=True,on_delete=models.CASCADE)
    file = models.FileField(upload_to="history/%Y/%m/%d", null=True, blank=True)
    date_time = models.DateTimeField(default=datetime.now())


class UseProduct(models.Model):
    task = models.ForeignKey(Task, null=False, blank=False,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, blank=False,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)


class Work(models.Model):
    employee = models.ForeignKey(Employee, null=False, blank=False,on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=False, blank=False,on_delete=models.CASCADE)
    time = models.DateTimeField()


User.company = property(lambda e: Company.objects.get(employee__pk=e.pk))  # NOQA
