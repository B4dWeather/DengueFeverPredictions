# Generated by Django 2.2.5 on 2021-02-18 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandemicsprediction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingoptions',
            name='regressor',
            field=models.BinaryField(default=None),
        ),
    ]
