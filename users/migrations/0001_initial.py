# Generated by Django 2.2 on 2019-07-19 13:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('GroupId', models.BigIntegerField(db_column='GROUP_ID', primary_key=True, serialize=False)),
                ('GroupName', models.TextField(db_column='GROUP_NAME', unique=True)),
                ('CreateUser', models.IntegerField(db_column='GROUP_CREATOR')),
                ('Owner', models.IntegerField(db_column='OWNER')),
                ('Manager', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='MANAGER', size=None)),
                ('Member', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='Member', size=None)),
            ],
            options={
                'db_table': 'user_group_info_base',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('UserId', models.AutoField(db_column='USER_ID', primary_key=True, serialize=False)),
                ('UserName', models.TextField(db_column='USER_NAME', unique=True)),
                ('UserPw', models.TextField(db_column='USER_PASSWORD')),
                ('UserEmail', models.TextField(db_column='USER_EMAIL')),
                ('UserPhone', models.CharField(db_column='USER_PHONE', max_length=11, unique=True)),
                ('DateTime', models.DateTimeField(auto_now_add=True, db_column='USER_TIME')),
                ('Is_Superuser', models.BooleanField(db_column='ROOT', default=False)),
                ('Is_Developer', models.BooleanField(db_column='DEV', default=False)),
                ('Is_Active', models.BooleanField(db_column='ACTIVE', default=True)),
                ('Is_Banned', models.BooleanField(db_column='BANNED', default=False)),
            ],
            options={
                'db_table': 'user_info_base',
            },
        ),
        migrations.CreateModel(
            name='UserCollection',
            fields=[
                ('UserId', models.IntegerField(db_column='USER_ID', primary_key=True, serialize=False)),
                ('Star', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), db_column='STAR', default=list, size=None)),
                ('CreateDoc', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), db_column='CREATE', default=list, size=None)),
                ('UploadSource', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), db_column='UPLOAD', default=list, size=None)),
            ],
            options={
                'db_table': 'user_collection',
            },
        ),
        migrations.CreateModel(
            name='UserConcern',
            fields=[
                ('UserId', models.IntegerField(db_column='USER_ID', primary_key=True, serialize=False)),
                ('SourceId', models.BigIntegerField(db_column='SOURCE_ID')),
                ('Labels', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), db_column='LABELS', default=list, size=None)),
                ('Imp', models.IntegerField(db_column='IMP', default=-1)),
                ('HardLevel', models.IntegerField(db_column='HARD_LEVEL', default=-1)),
                ('Useful', models.IntegerField(db_column='USEFUL', default=-1)),
            ],
            options={
                'db_table': 'user_labels',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('UserId', models.IntegerField(db_column='USER_ID', primary_key=True, serialize=False)),
                ('Is_Member', models.BooleanField(db_column='MEMBER', default=False)),
                ('Is_Organizer', models.BooleanField(db_column='ORGANIZER', default=False)),
            ],
            options={
                'db_table': 'user_info_role',
            },
        ),
    ]
