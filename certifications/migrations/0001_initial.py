# Generated by Django 4.2.5 on 2023-09-12 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('group', models.CharField()),
                ('name', models.CharField(max_length=15)),
                ('second_name', models.CharField(blank=True, max_length=15)),
                ('last_name', models.CharField(max_length=35)),
                ('second_surname', models.CharField(max_length=35)),
                ('reading', models.CharField(max_length=3)),
                ('listening', models.CharField(max_length=3)),
                ('writing', models.CharField(max_length=3)),
                ('speaking', models.CharField(max_length=3)),
                ('equivalent', models.CharField(max_length=35)),
                ('tomo', models.PositiveIntegerField()),
                ('folio', models.PositiveIntegerField()),
                ('decano', models.CharField(max_length=150)),
                ('court_president', models.CharField(max_length=150)),
                ('career', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('second_name', models.CharField(blank=True, max_length=15)),
                ('last_name', models.CharField(max_length=35)),
                ('second_surname', models.CharField(max_length=35)),
                ('facultad', models.PositiveIntegerField(default=1)),
            ],
        ),
    ]
