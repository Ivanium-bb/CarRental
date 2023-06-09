# Generated by Django 4.1.7 on 2023-03-15 12:33
import os

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    def generate_cars(apps, *args, **kwargs):
        from Main.models import Car
        Car.objects.create(is_available=True)
        Car.objects.create(is_available=True)
        Car.objects.create(is_available=True)
        Car.objects.create(is_available=True)
        Car.objects.create(is_available=True)

    operations = [

        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_start', models.DateField(blank=True)),
                ('session_finish', models.DateField(blank=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.car')),
            ],
        ),
        migrations.RunPython(generate_cars),

    ]
