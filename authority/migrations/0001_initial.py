# Generated by Django 2.2 on 2019-07-06 05:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAuthority',
            fields=[
                ('uuid', models.UUIDField(db_column='uuid', primary_key=True, serialize=False)),
                ('Owner', models.IntegerField(db_column='createUser')),
                ('ChangeState', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='changeStatePrivilege', default=list, size=None)),
                ('SharedTo', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='SharePrivilege', default=list, size=None)),
                ('query', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='readPrivilege', default=list, size=None)),
                ('write', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='writePrivilege', default=list, size=None)),
                ('reference', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='referencePrivilege', default=list, size=None)),
                ('delete', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='deletePrivilege', default=list, size=None)),
                ('export', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='exportPrivilege', default=list, size=None)),
                ('payment', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), db_column='payment', default=list, size=None)),
                ('source_type', models.TextField(db_column='type', default='Document')),
                ('Common', models.BooleanField(db_column='common', default=True)),
                ('Shared', models.BooleanField(db_column='shared', default=False)),
                ('Paid', models.BooleanField(db_column='paid', default=False)),
            ],
            options={
                'db_table': 'base_authority',
            },
        ),
    ]
