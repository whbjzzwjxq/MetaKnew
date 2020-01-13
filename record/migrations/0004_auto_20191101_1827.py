# Generated by Django 2.2 on 2019-11-01 18:27

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0003_auto_20191030_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='VersionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CreateUser', models.BigIntegerField(editable=False)),
                ('CreateTime', models.DateTimeField(auto_now_add=True)),
                ('SourceId', models.BigIntegerField(db_index=True, editable=False)),
                ('VersionId', models.IntegerField(default=1)),
                ('SourceType', models.TextField(editable=False)),
                ('SourceLabel', models.TextField(default='')),
                ('Content', django.contrib.postgres.fields.hstore.HStoreField(default=dict)),
            ],
            options={
                'db_table': 'history_node_version_record',
            },
        ),
        migrations.DeleteModel(
            name='ErrorRecord',
        ),
        migrations.DeleteModel(
            name='NodeVersionRecord',
        ),
        migrations.AddField(
            model_name='warnrecord',
            name='SourceType',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='warnrecord',
            name='BugType',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='warnrecord',
            name='CreateUser',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='warnrecord',
            name='Is_Solved',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='warnrecord',
            name='SourceId',
            field=models.BigIntegerField(db_index=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='warnrecord',
            name='SourceLabel',
            field=models.TextField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='warnrecord',
            name='WarnContent',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), default=list, size=None),
        ),
        migrations.AddIndex(
            model_name='versionrecord',
            index=models.Index(fields=['SourceId', 'SourceType', 'SourceLabel'], name='history_ver_SourceI_cc0796_idx'),
        ),
        migrations.AddConstraint(
            model_name='versionrecord',
            constraint=models.UniqueConstraint(fields=('SourceId', 'VersionId'), name='NodeVersionControl'),
        ),
    ]
