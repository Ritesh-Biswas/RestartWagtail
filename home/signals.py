from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import SubDepartmentPage

@receiver(post_save, sender=SubDepartmentPage)
def create_rbac_groups(sender, instance, created, **kwargs):
    if created:
        # Create groups
        general_user_group, _ = Group.objects.get_or_create(name=f"{instance.name}_general_user")
        editors_group, _ = Group.objects.get_or_create(name=f"{instance.name}_editors")
        moderators_group, _ = Group.objects.get_or_create(name=f"{instance.name}_moderators")

        # Assign site admins to the appropriate groups
        for admin in instance.site_admins.all():
            admin.groups.add(general_user_group)
            admin.groups.add(editors_group)
