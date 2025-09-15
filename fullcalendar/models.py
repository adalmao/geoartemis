from django.contrib.auth.models import Group, User
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext as _

# from aula_virtual.models import Company
# from proteccion_ambiental.settings import COMPANY_JRA_SLUG




class Calendar(models.Model):
    title = models.CharField(_('title'), max_length=200, null=False, blank=None)
    # company = models.ForeignKey(Company, related_name="company", null=False)
    slug = models.SlugField(max_length=100)
    users = models.ManyToManyField(User, related_name="users", verbose_name=_('shared with'),blank=True)
    created_by = models.ForeignKey(User, related_name="created_by",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Calendar')
        verbose_name_plural = _('Calendars')
        permissions = (
            ("view_calendars", "Can see existing calendars"),
        )

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(self.title)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exists = Calendar.objects.get(slug=slug)
                    if slug_exists:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Calendar.DoesNotExist:
                    self.slug = slug
                    break
        super(Calendar, self).save(*args, **kwargs)


class Accessibility(models.Model):
    calendar = models.ForeignKey(Calendar,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventType(models.Model):
    name = models.CharField(_('type'), max_length=200, null=False, blank=None)
    def __str__(self):
        return self.name


class Events(models.Model):
    calendar = models.ForeignKey(Calendar,on_delete=models.CASCADE)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    observation = models.TextField(blank=True, null=True)
    member = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.ForeignKey(EventType,on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name="created_by_event",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
