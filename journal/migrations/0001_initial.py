# Generated by Django 2.0.4 on 2018-04-24 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milage', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('date', models.DateTimeField()),
                ('comment', models.CharField(max_length=224)),
            ],
        ),
        migrations.CreateModel(
            name='ActionPopular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=224)),
            ],
        ),
        migrations.CreateModel(
            name='ActionTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=224)),
                ('action_milage_period', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('action_days_period', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('action_popular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.ActionPopular')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacurer', models.CharField(max_length=24)),
                ('model', models.CharField(max_length=24)),
                ('prod_year', models.DecimalField(decimal_places=0, max_digits=4, null=True)),
                ('engine_model', models.CharField(blank=True, max_length=24, null=True)),
                ('VIN', models.CharField(blank=True, max_length=30, null=True)),
                ('milage', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('fuel', models.CharField(choices=[('gasoline', 'gasoline'), ('diesel', 'diesel'), ('electricity', 'electricity'), ('hybrid', 'hybrid')], max_length=24)),
                ('power', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('torque', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
                ('engine_capacity', models.DecimalField(decimal_places=0, max_digits=9)),
            ],
            options={
                'ordering': ['manufacurer', 'model', 'engine_capacity'],
            },
        ),
        migrations.CreateModel(
            name='CarOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('surname', models.CharField(max_length=24)),
                ('nick', models.CharField(blank=True, max_length=24, null=True)),
                ('email', models.CharField(blank=True, max_length=24, null=True)),
                ('phone_tel', models.CharField(blank=True, max_length=24, null=True)),
                ('SlackCon', models.CharField(blank=True, max_length=24, null=True)),
                ('FBCon', models.CharField(blank=True, max_length=24, null=True)),
            ],
            options={
                'ordering': ['surname', 'name'],
            },
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ManyToManyField(to='journal.CarOwner'),
        ),
        migrations.AddField(
            model_name='actiontemplate',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.Car'),
        ),
        migrations.AddField(
            model_name='action',
            name='ActionTemplate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.ActionTemplate'),
        ),
    ]
