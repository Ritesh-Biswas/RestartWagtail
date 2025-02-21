from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel,MultipleChooserPanel
from django.contrib.auth.models import User
from modelcluster.fields import ParentalManyToManyField
from django import forms 
from modelcluster.fields import ParentalKey


class HomePage(Page):
    template = 'home/home_page.html' #this is used to specify the template for the page

    subpage_types = ['home.DepartmentPage'] #this is for making sure that only DepartmentPage can be created as a child page of HomePage

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
    subpage_types = ['home.AnnouncementPage', 'home.FAQPage']  

    class Meta:
        verbose_name = "Sub Department"
        verbose_name_plural = "Sub Departments"


class AnnouncementPage(Page):
    name = models.CharField(max_length=200)
    description = RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
    ]

    template = 'home/announcement_page.html'
    parent_page_types = ['home.SubDepartmentPage']
    subpage_types = []  # No child pages allowed
    
    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ['-date_posted']

class FAQPage(Page):
    question = models.CharField(max_length=200)
    answer = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    template = 'home/faq_page.html'
    parent_page_types = ['home.SubDepartmentPage']
    subpage_types = []  # No child pages allowed

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"