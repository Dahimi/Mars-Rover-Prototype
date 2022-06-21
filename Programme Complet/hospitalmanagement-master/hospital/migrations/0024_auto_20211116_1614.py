# Generated by Django 3.2 on 2021-11-16 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0023_infirmier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockName', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.block')),
            ],
        ),
        migrations.DeleteModel(
            name='Infirmier',
        ),
    ]
