# Generated by Django 3.2 on 2021-12-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0030_auto_20211214_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='bed',
            name='patientId',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
