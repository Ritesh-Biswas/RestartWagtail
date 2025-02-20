from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


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

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
