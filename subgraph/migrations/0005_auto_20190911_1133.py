# Generated by Django 2.2 on 2019-09-11 03:33

import django.core.validators
from django.db import migrations
import tools.models


class Migration(migrations.Migration):

    dependencies = [
        ('subgraph', '0004_auto_20190911_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medianode',
            name='Description',
        ),
        migrations.AddField(
            model_name='medianode',
            name='Hot',
            field=tools.models.HotField(default=100, validators=[django.core.validators.MinValueValidator(limit_value=1)]),
        ),
        migrations.AlterField(
            model_name='nodectrl',
            name='Hot',
            field=tools.models.HotField(default=100, validators=[django.core.validators.MinValueValidator(limit_value=1)]),
        ),
        migrations.AlterField(
            model_name='text',
            name='Hot',
            field=tools.models.HotField(default=100, validators=[django.core.validators.MinValueValidator(limit_value=1)]),
        ),
    ]
