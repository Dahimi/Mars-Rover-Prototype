# Generated by Django 3.2 on 2021-12-14 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0028_alter_patient_isaffected'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='cin',
            field=models.CharField(default='Pas de CIN', max_length=20),
            preserve_default=False,
        ),
    ]