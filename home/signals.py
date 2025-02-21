from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from wagtail.models import Page
from wagtail.images.models import Image
from wagtail.documents.models import Document
from django.contrib.contenttypes.models import ContentType
from .models import SubDepartmentPage

@receiver(post_save, sender=SubDepartmentPage)
def create_rbac_groups(sender, instance, created, **kwargs):
    if created:
        # Create RBAC groups based on SubDepartmentPage instance name
        general_user_group, _ = Group.objects.get_or_create(name=f"{instance.name}_general_user")
        editors_group, _ = Group.objects.get_or_create(name=f"{instance.name}_editors")
        moderators_group, _ = Group.objects.get_or_create(name=f"{instance.name}_moderators")

        # Assign site admins to the created groups
        for admin in instance.site_admins.all():
            admin.groups.add(general_user_group, editors_group, moderators_group)

        # Add Wagtail Admin access permission
        try:
            wagtail_admin_permission = Permission.objects.get(codename="access_admin")
            editors_group.permissions.add(wagtail_admin_permission)
            moderators_group.permissions.add(wagtail_admin_permission)
        except Permission.DoesNotExist:
            print("⚠️ Warning: 'access_admin' permission not found!")

        print(f"✅ RBAC groups and permissions assigned for '{instance.name}' successfully!")

@receiver(post_delete, sender=SubDepartmentPage)
def delete_rbac_groups(sender, instance, **kwargs):
    # Delete RBAC groups based on SubDepartmentPage instance name
    Group.objects.filter(name=f"{instance.name}_general_user").delete()
    Group.objects.filter(name=f"{instance.name}_editors").delete()
    Group.objects.filter(name=f"{instance.name}_moderators").delete()

    print(f"🗑️ RBAC groups for '{instance.name}' deleted successfully!")
