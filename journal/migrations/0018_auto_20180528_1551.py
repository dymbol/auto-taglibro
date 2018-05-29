# Generated by Django 2.0.4 on 2018-05-28 15:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0002_logentry_remove_auto_add'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('journal', '0017_remove_carowner_nick'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarOwner',
            new_name='Owner',
        ),
    ]
