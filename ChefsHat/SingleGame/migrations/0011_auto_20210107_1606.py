# Generated by Django 3.0.5 on 2021-01-07 16:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SingleGame', '0010_auto_20210107_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='Qvalues',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=8), default=list, size=None),
        ),
    ]
