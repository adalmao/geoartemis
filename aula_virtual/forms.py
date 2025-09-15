import datetime
from django import forms
from django.forms import ModelForm, HiddenInput
from django.utils.translation import ugettext, ugettext_lazy as _
from djrichtextfield.models import RichTextField
from djrichtextfield.widgets import RichTextWidget

from aula_virtual.functions import add_form_control_class, add_form_text,add_class_time_picker
from .models import Company, Format, Accident, Employee, Course, Package, Package_User_Course, EspecificCourse, \
    Capacitacion, CapacitationDetail, Service, ServiceDetail


class FormatForm(ModelForm):
    # file = forms.FileField(required=True)

    class Meta:
        model = Format
        fields = ['name', 'file', 'type_format']

    def __init__(self, *args, **kwargs):
        super(FormatForm, self).__init__(*args, **kwargs)
        add_form_control_class(self.fields)

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        add_form_text(self, ('ruc',))
        add_form_control_class(self.fields)


class EmployeeForm(ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    username = forms.CharField(widget=forms.HiddenInput(), required=False, label='')

    class Meta:
        model = Employee
        fields = ('code', 'first_name', 'last_name', 'email', 'password1', 'password2', 'username')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget = HiddenInput()
        # self.fields['username'].label = ''
        add_form_control_class(self.fields)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(EmployeeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class AccidentForm(ModelForm):
    class Meta:
        model = Accident
        fields = ['title', 'content', 'type_accident', 'date', 'evidence']

    def __init__(self, *args, **kwargs):
        super(AccidentForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)


class ProductForm(ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
        self.fields['title'].label = 'Nombre Paquete: '
        self.fields['price'].label = 'Precio: ($/.) '
        self.fields['count_mounth'].label = 'Cantidad de meses: '
        self.fields['is_active'].label = 'Activo: '


class Package_User_CourseForm(ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = Package_User_Course
        fields = ['package', 'file']

    def __init__(self, *args, **kwargs):
        super(Package_User_CourseForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        self.fields['package'].label = 'Escoga su paquete: '
        self.fields['file'].label = 'Subir Voucher: '
        add_form_control_class(self.fields)


class CourseForm(ModelForm):
    video=forms.URLField(label='video',initial='http://')
    class Meta:
        model = Course
        fields = ['name', 'description', 'file','video']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        self.fields['video'].required=False
        add_form_control_class(self.fields)



class EspecificCourseForm(ModelForm):
    video = forms.FileField(required=False)

    class Meta:
        model = EspecificCourse
        exclude = ['course', 'is_active','zoom']

    def __init__(self, *args, **kwargs):
        super(EspecificCourseForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
        add_class_time_picker(self, ['start_date'])


class CapacitationForm(ModelForm):
    class Meta:
        model = Capacitacion
        fields = ['name', 'file']

    def __init__(self, *args, **kwargs):
        super(CapacitationForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)


class CapacitationDetailForm(ModelForm):
    class Meta:
        model = CapacitationDetail
        fields = ['descrip']

    def __init__(self, *args, **kwargs):
        super(CapacitationDetailForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'file']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)


class ServiceDetailForm(ModelForm):
    class Meta:
        model = ServiceDetail
        fields = ['descrip']

    def __init__(self, *args, **kwargs):
        super(ServiceDetailForm, self).__init__(*args, **kwargs)
        _instance = kwargs.pop('instance', None)
        add_form_control_class(self.fields)
