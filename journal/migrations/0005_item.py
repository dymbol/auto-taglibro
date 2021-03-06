# Generated by Django 2.2.13 on 2020-06-22 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_car_enable_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=224, null=True)),
                ('producer', models.CharField(blank=True, max_length=224, null=True)),
                ('PN', models.CharField(blank=True, max_length=224, null=True)),
                ('similar_product', models.CharField(blank=True, max_length=224, null=True)),
                ('SN', models.CharField(blank=True, max_length=224, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity_unit', models.CharField(blank=True, max_length=24, null=True)),
                ('description', models.CharField(blank=True, max_length=224, null=True)),
                ('seller', models.CharField(blank=True, max_length=128, null=True)),
                ('bill_no', models.CharField(blank=True, max_length=24, null=True)),
                ('buy_date', models.DateField()),
                ('cost', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.Action')),
            ],
        ),
    ]
