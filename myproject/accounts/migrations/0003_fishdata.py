# Generated by Django 5.0.6 on 2024-06-26 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_fishnumber_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='FishData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=100)),
                ('weight', models.FloatField()),
                ('length', models.FloatField()),
                ('height', models.FloatField()),
                ('width', models.FloatField()),
            ],
        ),
    ]