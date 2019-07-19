# Generated by Django 2.2 on 2019-07-19 13:47

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelRecord',
            fields=[
                ('uuid', models.BigIntegerField(db_column='UUID', primary_key=True, serialize=False)),
                ('ExcelURL', models.URLField(db_column='URL')),
                ('UserId', models.IntegerField(db_column='USER_ID')),
                ('Nodes', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), db_column='NODES', size=None)),
            ],
            options={
                'db_table': 'history_excel_upload',
            },
        ),
        migrations.CreateModel(
            name='SourceAddRecord',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('Is_Error', models.BooleanField(db_column='ERROR', default=False)),
                ('Is_Warn', models.BooleanField(db_column='WARN', default=False)),
                ('SourceId', models.BigIntegerField(db_column='UUID')),
                ('SourceType', models.TextField(db_column='TYPE')),
                ('Content', django.contrib.postgres.fields.jsonb.JSONField(db_column='CONTENT', default=dict)),
                ('Time', models.DateTimeField(auto_now_add=True, db_column='TIME')),
            ],
            options={
                'db_table': 'history_source_add_record',
            },
        ),
        migrations.CreateModel(
            name='UserEditRecord',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('EditTarget', models.BigIntegerField(db_column='')),
                ('EditTime', models.DateTimeField(auto_now_add=True, db_column='TIME')),
            ],
        ),
        migrations.CreateModel(
            name='VersionRecord',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('SourceId', models.BigIntegerField(db_column='UUID')),
                ('SourceType', models.TextField(db_column='TYPE')),
                ('Content', models.IntegerField(db_column='VERSION')),
            ],
            options={
                'db_table': 'history_version_record',
            },
        ),
    ]
