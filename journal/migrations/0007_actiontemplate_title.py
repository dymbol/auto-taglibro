# Generated by Django 2.0.4 on 2018-05-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0006_auto_20180511_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='actiontemplate',
            name='title',
            field=models.CharField(default='ddfed', max_length=32),
            preserve_default=False,
        ),
    ]
