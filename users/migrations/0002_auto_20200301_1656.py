# Generated by Django 3.0.3 on 2020-03-01 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Email',
            field=models.TextField(db_index=True, null=True, unique=True),
        ),
    ]