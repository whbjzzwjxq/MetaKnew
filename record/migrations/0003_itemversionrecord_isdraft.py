# Generated by Django 3.0.3 on 2020-02-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_auto_20200226_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemversionrecord',
            name='IsDraft',
            field=models.BooleanField(default=True),
        ),
    ]
