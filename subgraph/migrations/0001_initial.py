# Generated by Django 2.2 on 2019-07-06 05:20

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('uuid', models.UUIDField(db_column='UUID', editable=False, primary_key=True, serialize=False)),
                ('Imp', models.IntegerField(db_column='IMP', default=0)),
                ('Hot', models.IntegerField(db_column='HOT', default=0)),
                ('StrLevel', models.FloatField(db_column='STR', default=0)),
                ('ClaLevel', models.IntegerField(db_column='CLA', default=0)),
                ('ImportMethod', models.CharField(db_column='IMPORT_METHOD', max_length=30)),
                ('ImportTime', models.DateTimeField(db_column='IMPORT_TIME', default=django.utils.timezone.now)),
                ('IncludedMedia', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), db_column='INCLUDED_MEDIA', default=list, size=None)),
                ('FeatureVec', models.TextField(db_column='FEATURE_VECTOR', default='0')),
                ('CreateUser', models.IntegerField(db_column='USER', default='0')),
                ('Is_Common', models.BooleanField(db_column='COMMON', default=True)),
                ('Is_Used', models.BooleanField(db_column='USED', default=True)),
            ],
            options={
                'db_table': 'base_node',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subgraph.Node')),
                ('PeriodStart', models.DateField(db_column='PERIOD_START')),
                ('PeriodEnd', models.DateField(db_column='PERIOD_END')),
                ('BirthPlace', models.CharField(db_column='BIRTHPLACE', max_length=30)),
                ('Nation', models.CharField(db_column='NATION', default='None', max_length=30)),
            ],
            options={
                'db_table': 'person',
            },
            bases=('subgraph.node',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subgraph.Node')),
                ('PeriodStart', models.DateField(db_column='PERIOD_START')),
                ('PeriodEnd', models.DateField(db_column='PERIOD_END')),
                ('Location', models.TextField(db_column='LOCATION')),
                ('Longitude', models.FloatField(db_column='LONGITUDE', default=0)),
                ('Latitude', models.FloatField(db_column='LATITUDE', default=0)),
                ('Nation', models.TextField(db_column='NATION', max_length=30)),
            ],
            options={
                'db_table': 'project',
            },
            bases=('subgraph.node',),
        ),
        migrations.CreateModel(
            name='ArchProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subgraph.Project')),
                ('Architect', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), db_column='ARCHITECT', size=None)),
            ],
            options={
                'db_table': 'arch_project',
            },
            bases=('subgraph.project',),
        ),
    ]
