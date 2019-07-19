from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
# Create your models here.


class MediaNode(models.Model):
    id = models.Field(db_column='ID', primary_key=True)
    FileName = models.TextField(db_column='NAME')
    Format = models.TextField(db_column='FORMAT')
    Url = models.URLField(db_column='URL', default='')
    UploadUser = models.IntegerField(db_column='UPLOAD_USER')
    UploadTime = models.DateTimeField(db_column='UPLOAD_TIME', auto_now_add=True)
    Description = models.TextField(db_column='DESCRIPTION', default='None')
    AbbrPic = models.URLField(db_column='CONTENT', default='')

    class Meta:

        db_table = 'media_base'


class Paper(MediaNode):
    Tags = ArrayField(JSONField(), db_column='TAGS', default=list)
    Rels = ArrayField(JSONField(), db_column='RELS', default=list)

    class Meta:
        db_table = 'paper'