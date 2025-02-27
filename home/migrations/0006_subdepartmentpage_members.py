# Generated by Django 5.1.6 on 2025-02-21 09:34

import modelcluster.fields
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_announcementpage_faqpage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subdepartmentpage',
            name='members',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, limit_choices_to={'is_superuser': False}, related_name='department_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
