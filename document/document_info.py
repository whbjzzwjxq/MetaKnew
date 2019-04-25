# -*-coding=utf-8 -*-
from document import models
import datetime as dt


def add(filedata={}):

    doc = models.Document_Information.objects.create(**filedata)
    return doc


# id 表示专题uuid
def selectById(uuid):
    assert uuid
    doc = models.Document_Information.objects.filter(uuid=uuid)
    return doc

# 查询所有专题信息的uuid和title
def selectAll():
    doc = models.Document_Information.objects.all().values('uuid','title')
    return doc

# 查询专题包含的多媒体文件
def selectURLById(uuid):
    doc = models.Document_Information.objects.filter(uuid=uuid)
    return doc


# ID 表示专题id
def updateById(id,filedata={}):
    assert id
    update_field = {}
    for filename in filedata:
        update_field['Document.'+filename] = filedata[filename]
    res = models.Document_Information.objects.filter(uuid=id).update(update_field)
    return res

# 更新专题多媒体文件
def updateURLById(id, medias = []):
    assert id
    res = models.Document_Information.objects.filter(uuid=id).update(included_media=medias)
    return res

# ID 表示专题id not专题uuid
def deleteById(id):
    assert id
    res = models.Document_Information.objects.filter(id=id).delete()
    return res
