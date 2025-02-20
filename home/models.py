from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel,MultipleChooserPanel
from django.contrib.auth.models import User
from modelcluster.fields import ParentalManyToManyField
from django import forms 


class HomePage(Page):
    template = 'home/home_page.html'

    subpage_types = ['home.DepartmentPage']

class DepartmentPage(Page):
    dept_name = models.CharField(max_length=100)
    description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('dept_name'),
        FieldPanel('description'),
    ]

    template = 'home/department_page.html'
    subpage_types = ['home.SubDepartmentPage']

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class SubDepartmentPage(Page):
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True)
    site_admins = ParentalManyToManyField(
        User,
        related_name='administered_subdepartments',
        blank=True,
        limit_choices_to={'is_superuser': False}
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('site_admins', widget=forms.CheckboxSelectMultiple),
    ]

    template = 'home/sub_department_page.html'
    parent_page_types = ['home.DepartmentPage']
    subpage_types = []  # No child pages allowed

    class Meta:
        verbose_name = "Sub Department"
        verbose_name_plural = "Sub Departments"