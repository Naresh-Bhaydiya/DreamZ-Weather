# Generated by Django 4.2.7 on 2023-12-03 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=255)),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]