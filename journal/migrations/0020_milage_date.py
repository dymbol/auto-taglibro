# Generated by Django 2.0.4 on 2018-06-11 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0019_auto_20180611_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='milage',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]