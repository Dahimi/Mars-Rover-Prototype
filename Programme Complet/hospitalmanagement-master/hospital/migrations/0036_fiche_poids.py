# Generated by Django 3.2 on 2021-12-15 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0035_fiche'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiche',
            name='poids',
            field=models.CharField(default='', max_length=10),
        ),
    ]
