# Generated by Django 2.2 on 2019-07-19 13:47

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocationDoc',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('Name', models.TextField(db_column='NAME', default='Beijing')),
                ('LocId', models.TextField(db_column='LOC_ID', default='ChIJ58KMhbNLzJQRwfhoMaMlugA')),
                ('Alias', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), db_column='ALIAS', default=list, size=None)),
                ('Doc', django.contrib.postgres.fields.jsonb.JSONField(db_column='DOC', default=dict)),
            ],
            options={
                'db_table': 'location_doc',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('ImportMethod', models.CharField(db_column='IMPORT_METHOD', editable=False, max_length=30)),
                ('ImportTime', models.DateTimeField(auto_now_add=True, db_column='IMPORT_TIME')),
                ('CreateUser', models.IntegerField(db_column='USER', default='0', editable=False)),
                ('Is_Common', models.BooleanField(db_column='COMMON', default=True)),
                ('Is_Used', models.BooleanField(db_column='USED', default=True)),
                ('Imp', models.IntegerField(db_column='IMP', default=0)),
                ('Hot', models.IntegerField(db_column='HOT', default=0)),
                ('StrLevel', models.FloatField(db_column='STR', default=0)),
                ('ClaLevel', models.IntegerField(db_column='CLA', default=0)),
                ('FeatureVec', models.TextField(db_column='FEATURE_VECTOR', default='0')),
                ('IncludedMedia', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), db_column='INCLUDED_MEDIA', default=list, size=None)),
                ('History', models.IntegerField(db_column='HISTORY')),
                ('Contributor', django.contrib.postgres.fields.JSONField(db_column='CONTRIBUTOR')),
                ('id', models.BigIntegerField(db_column='ID', editable=False, primary_key=True, serialize=False)),
                ('Name', models.TextField(db_column='NAME')),
                ('PrimaryLabel', models.TextField(db_column='P_LABEL', editable=False)),
                ('Alias', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), db_column='ALIAS', default=list, size=None)),
                ('Description', models.TextField(db_column='DESCRIPTION', default='')),
            ],
            options={
                'db_table': 'node_base',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subgraph.Node')),
                ('PeriodStart', models.TextField(db_column='PERIOD_START')),
                ('PeriodEnd', models.TextField(db_column='PERIOD_END')),
                ('BirthPlace', models.CharField(db_column='BIRTHPLACE', max_length=30)),
                ('Nation', models.CharField(db_column='NATION', default='None', max_length=30)),
            ],
            options={
                'db_table': 'node_person',
            },
            bases=('subgraph.node',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subgraph.Node')),
                ('PeriodStart', models.TextField(db_column='PERIOD_START')),
                ('PeriodEnd', models.TextField(db_column='PERIOD_END')),
                ('Nation', models.TextField(db_column='NATION', max_length=30)),
                ('Leader', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), db_column='LEADER', default=list, size=None)),
            ],
            options={
                'db_table': 'node_project',
            },
            bases=('subgraph.node',),
        ),
        migrations.CreateModel(
            name='ArchProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subgraph.Project')),
                ('Location', models.TextField(db_column='LOCATION', default='Beijing')),
                ('WorkTeam', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), db_column='WORK_TEAM', default=list, size=None)),
            ],
            options={
                'db_table': 'node_arch_project',
            },
            bases=('subgraph.project',),
        ),
    ]
