# Generated by Django 2.0.4 on 2018-08-21 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0025_actiontemplate_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.File'),
        ),
    ]
