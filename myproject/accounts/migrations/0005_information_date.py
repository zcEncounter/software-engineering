# Generated by Django 5.0.6 on 2024-06-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=1, verbose_name='Date'),
            preserve_default=False,
        ),
    ]
