# Generated by Django 2.2 on 2019-10-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subgraph', '0003_mediactrl_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediactrl',
            name='PrimaryLabel',
            field=models.TextField(db_index=True, default=''),
        ),
    ]