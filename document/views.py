# -*-coding=utf-8 -*-
# APP内定义
from tools.base_tools import get_dict
from document.logic_class import BaseComment
# django定义与工具包
import datetime as dt
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from demo import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os
from tools.location import getHttpResponse
from django.forms.models import model_to_dict
from django.core.cache import cache
from document.logic_class import PersonalDoc


# Create your views here.
@csrf_exempt
# 根据专题id得到个人化的信息
def get_personal_by_doc(request):
    doc_id = request.GET.get('uuid')
    user = request.GET.get('user_id')
    result = PersonalDoc(uuid=doc_id, user=user).query_all()
    return HttpResponse(json.dumps(result), content_type="application/json")


# 添加评论
@csrf_exempt
def add_comment(request):
    data = json.loads(request.body)['data']
    uuid = request.GET.get('uuid')
    user_id = request.GET.get('user_id')
    if data['content'] == '':
        return HttpResponse("评论不能为空")
    else:
        BaseComment().add(
            base=uuid,
            target=data['target'],
            user=user_id,
            content=str(data['content']),
            time=dt.datetime.now()
        )

    return HttpResponse("回复成功")


# 根据commentId删除评论
@csrf_exempt
def delete_comment(request):
    uuid = request.GET.get('uuid')
    if uuid == '':
        return HttpResponse(getHttpResponse('0', '删除失败', ''), content_type='application/json')
    else:
        comment = BaseComment().query(uuid=uuid)
        comment.delete()
    return HttpResponse(getHttpResponse('1', '删除成功', ''), content_type="application/json")


# 上传文件        已测试---4.18-----ZXN
# 文件预览路径127.0.0.1:8000/media/files/upload/ + 文件名
def upload_file(request):
    response = HttpResponse()
    uuid = request.POST.get("uuid")
    user_id = request.GET.get('user_id')
    my_file = request.FILES.get("my_file", None)
    if not my_file:
        respData = {'status': '0', 'ret': '没有可上传的文件！！！'}
    else:
        if os.sep in my_file.name:
            respData = {'status': '1', 'ret': r"""请注意文件命名格式，'\ / " * ? < > '符号文件不允许上传。"""}
        else:
            myfilepath = settings.BASE_DIR + os.sep + "files" + os.sep + "upload" + os.sep + my_file.name
            print(myfilepath)
            docs = document_info.selectURLById(uuid)
            for doc in docs:
                names = doc.included_media
                print(names)
                if names != None:
                    if my_file.name in names:
                        respData = {'status': '2', 'ret': '该文件已存在,请勿重复上传'}
                    else:
                        with open(myfilepath, 'wb+') as f:
                            for chunk in my_file.chunks():  # 分块写入文件
                                f.write(chunk)
                        names.append(my_file.name)
                        document_info.updateURLById(uuid, names)
                        respData = {'status': '3', 'ret': '上传成功！！！'}
                else:
                    with open(myfilepath, 'wb+') as f:
                        for chunk in my_file.chunks():  # 分块写入文件
                            f.write(chunk)
                    names = []
                    print(str(my_file.name))
                    names.append(str(my_file.name))
                    print(names)
                    document_info.updateURLById(uuid, names)
                    respData = {'status': '3', 'ret': '上传成功！！！'}
    resp.content = json.dumps(respData)
    return HttpResponse(resp, content_type="application/json")


# 下载文件                         已测试------4.18-----ZXN
def download_file(request):
    resp = HttpResponse()
    uuid = request.POST.get("uuid", "")
    fileName = request.POST.get("fileName", "")
    docs = document_info.selectURLById(uuid)
    for doc in docs:
        names = doc.included_media
        print(names)
        print(fileName)
        if fileName in names:
            the_file_name = settings.BASE_DIR + os.sep + "files" + os.sep + "upload" + os.sep + fileName
            file = open(the_file_name, 'rb')
            # response = StreamingHttpResponse(file_iterator(url))
            response = StreamingHttpResponse(file)
            response['Content-Type'] = 'application/octet-stream; charset=unicode'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(
                fileName))  # escape_uri_path()解决中文名文件(from django.utils.encoding import escape_uri_path)
            return response


# 删除文件             已测试---4.18-----ZXN
def delete_file(request):
    resp = HttpResponse()
    uuid = request.POST.get("uuid", "")
    fileName = request.POST.get("fileName", "")
    docs = document_info.selectURLById(uuid)
    for doc in docs:
        names = doc.included_media
        if fileName in names:
            names.remove(fileName)
            document_info.updateURLById(uuid, names)
            the_file_name = settings.BASE_DIR + os.sep + "files" + os.sep + "upload" + os.sep + fileName
            if os.path.exists(the_file_name):
                os.remove(the_file_name)
                respData = {'status': '1', 'ret': '删除成功！！！'}
            else:
                respData = {'status': '0', 'ret': "文件不存在，删除失败,请于管理员联系。"}
        else:
            respData = {'status': '0', 'ret': "文件不存在，删除失败,请于管理员联系。"}
    resp.content = json.dumps(respData)
    return HttpResponse(resp, content_type="application/json")


def get_cache_doc(uuid_list):
    cache_docs = []
    for uuid in uuids:
        doc = list(document_info.selectById(uuid)[:1])
        cache_doc = {}
        if doc:
            doc = get_dict(doc[0])
            keys_in_store = ['title', 'url', 'hard_level', 'imp', 'uuid', 'area', 'size']
            for key in keys_in_store:
                cache_doc.update({key: str(doc[key])})
            cache_doc.update({'type': 'document'})
        if cache_doc:
            cache_docs.append(cache_doc)
    return cache_docs


# redis 测试存数据
def select_top(request):
    docs = models.DocumentInformation.objects.filter().order_by('id')[:3]
    filedata = {}
    for doc in docs:
        filedata['title'] = doc.title
        filedata['url'] = doc.url
        filedata['hard_level'] = doc.hard_level
        filedata['imp'] = doc.imp
        filedata['area'] = doc.area
        filedata['size'] = doc.size
        cache.set(doc.uuid, filedata, 60 * 60)
    return HttpResponse("成功！！！", content_type="application/json")


# 测试从redis中读取数据
def selectFromRedis(request):
    docs = models.DocumentInformation.objects.filter().order_by('id')[:3]
    res = []
    for doc in docs:
        res.append(cache.get(doc.uuid))
    return HttpResponse(res, content_type="application/json")


# 新增专题
def add_document(request):
    if request.method == 'POST':
        data = json.loads(request.body, encoding='utf-8')['data']
        # 专题节点与关系
        nodes = data['nodes']
        relationships = data['relationships']

        # 专题信息
        info = data['info']

        # 预定义容器
        doc_nodes = []
        doc_relationships = []
        Doc2Nodes = []
        node_index = {}

        for node in nodes:
            # 记录新建节点自动赋予的uuid
            old_id = node['info']['uuid']
            new_node = handle_node(node['info'])
            node_index.update({old_id: new_node})

            # 记录专题内节点坐标
            conf = {'uuid': new_node['uuid'], 'conf': node['conf']}
            doc_nodes.append(conf)

            # 先记录下节点和专题的相关性
            if new_node['Name'] in info['keywords']:
                Doc2Nodes.append({'type': 'Doc2Node', 'rate': 0.5, 'source': new_node})

        for relationship in relationships:
            # 从node_index里访问提交后的Node对象
            relationship["info"]['source'] = node_index[relationship["info"]['source']]
            relationship["info"]['target'] = node_index[relationship["info"]['target']]
            new_rel = handle_relationship(relationship['info'])
            conf = {'uuid': new_rel['uuid'], 'conf': relationship['conf']}
            doc_relationships.append(conf)
        # 新建专题
        new_document = {'Name': info['title'],
                        'PrimaryLabel': 'Document',
                        'Area': info['area'],
                        'type': "Document",
                        "nodes": doc_nodes,
                        "relationships": doc_relationships
                        }
        new_document = create_node(new_document)

        # 生成专题节点后再生成专题与普通节点的关系
        for Doc2Node in Doc2Nodes:
            Doc2Node.update({'target': new_document})
            handle_relationship(Doc2Node)

        # DocumentInformation部分
        data['info']['uuid'] = new_document['uuid']
        new_document_info = DocumentInformation()
        for key in get_dict(new_document_info):
            if key in data["info"]:
                setattr(new_document_info, key, data["info"][key])
        new_document_info.save()
        return HttpResponse('Create Document Success')


# 获取专题
def get_document(request):
    if request.method == 'POST':
        uuid = json.loads(request.body, encoding='utf-8')['data']['uuid']
        doc = document.selectById(uuid)
        return HttpResponse(json.dumps(model_to_dict(doc[0])), content_type="application/json")


# Create your views here.

# 新增路径               已测试-----4.24-----ZXN
def add_path(request):
    """
    	"data":{
		"path_title":"计算机",
		"path_document":[
			{"uuid":"b81cb129-9631-4d2f-9af0-74b8c56af8d5","order":"1","time":"200"},
			{"uuid":"3ad90c1a-601a-4d24-a22b-9931d6b5174c","order":"2","time":"300"},
			{"uuid":"3ad90c1a-601a-4d24-a22b-9931d6b5174c","order":"2","time":"300"},
			{"uuid":"924d061c-5517-11e9-9703-04d3b0eb8835","order":"3", "time":"100"}
		],
		"path_info":{
			"create_user":"2",
			"imp":"0.94",
			"hard_level":"0.99"
		}
	}
    """
    param = json.loads(request.body)['data']
    resp = HttpResponse()
    paths.add(param)
    respData = {'status': '1', 'ret': '添加成功!!!'}
    resp.content = json.dumps(respData)
    return HttpResponse(resp, content_type="application/json")


# 依据路径id查询路径，redis里有缓存的，则从redis里返回，没有则从数据库表里查找数据返回        已测试-----4.24-----ZXN
def showAllPath(request):
    param = json.loads(request.body)['data']
    path_id = param['path_id']
    path = paths.showById(path_id)
    res = []
    for p in path:
        documents = p.path_document
        for doc in documents:
            doc_info = json.loads(doc)
            # print(doc_info)
            doc_uuid = doc_info['uuid']
            if cache.has_key(doc_uuid):
                res.append(cache.get(doc_uuid))
                # print(1)
            else:
                docs = document_info.selectById(doc_uuid)
                for doc in docs:
                    doc.uuid = str(doc.uuid)
                    doc.time = str(doc.time)
                    res.append(dict(model_to_dict(doc).items()))
                    # print(2)
    return HttpResponse(json.dumps(res), content_type="application/json")


# 新增路径
def add(filedata={}):
    path = models.Path.objects.create(**filedata)
    return path


# 查询全部路径列表
def showById(path_id):
    assert path_id
    paths = models.Path.objects.filter(path_id=path_id)
    return paths


# Create your views here.

# 添加便签         已测试-----4.19----ZXN
def add_note(request):
    """
        "data":{
        "user_id":
        "tags_type":
        "content":
        "document_id":
    }
    """
    param = json.loads(request.body)['data']
    resp = HttpResponse()
    note_info.add(param)
    respData = {'status': '1', 'ret': '添加成功!!!'}
    resp.content = json.dumps(respData)
    return HttpResponse(resp, content_type="application/json")


# 删除便签         已测试-----4.19----ZXN
def delete_note(request):
    param = json.loads(request.body)['data']
    resp = HttpResponse()
    note_info.deleteById(param['id'])
    respData = {'status': '1', 'ret': '删除成功！！！'}
    resp.content = json.dumps(respData)
    return HttpResponse(resp, content_type="application/json")


# 更新便签         已测试-----4.19----ZXN
def update_note(request):
    """
     "data": {
         "id":
         "user_id":
         "tags_type":
         "content":
         "document_id":
     }
     :param filedata:
     :return:
     """
    param = json.loads(request.body)['data']
    resp = HttpResponse()
    note_info.updateById(param)
    respData = {'status': '1', 'ret': '更新成功！！！'}
    resp.content = json.dumps(respData)
    return HttpResponse(resp, content_type="application/json")


# 显示便签         已测试-----4.19----ZXN
def show_note(request):
    """
       "data":{
           "user_id":
           "document_id":
       }
       :param request:
       :return:
       """
    param = json.loads(request.body)['data']
    notes = note_info.selectByUserId(param['user_id'], param['document_id'])
    res = []
    for note in notes:
        note.document_id = str(note.document_id)
        res.append(dict(model_to_dict(note).items()))
    return HttpResponse(json.dumps(res), content_type="application/json")


# 添加便签
def add(filedata={}):
    notes = models.Note.objects.create(**filedata)
    return notes


# 删除便签
def deleteById(id):
    assert id
    notes = models.Note.objects.filter(id=id).delete()
    return notes


# 更新便签
def updateById(filedata={}):
    id = filedata['id']
    notes = models.Note.objects.filter(id=id).update(**filedata)
    return notes


# 依据用户id和专题uuid查询便签, document_id代表专题的uuid
def selectByUserId(user_id, document_id):
    assert user_id, document_id
    notes = models.Note.objects.filter(user_id=user_id, document_id=document_id)
    return notes


# -*-coding=utf-8 -*-
from document import models


def add(filedata={}):
    doc = models.DocumentInformation.objects.create(**filedata)
    return doc


# id 表示专题uuid
def selectById(uuid, user_id, level):
    assert uuid
    result = Authority.checkAuth(uuid, user_id, level)
    if result is True:
        doc = models.Document_Information.objects.filter(uuid=uuid)
        return True
    else:
        return False


# 查询所有专题信息的uuid和title
def selectAll():
    doc = models.DocumentInformation.objects.all().values('uuid', 'title')
    return doc


# 查询专题包含的多媒体文件
def selectURLById(uuid):
    doc = models.DocumentInformation.objects.filter(uuid=uuid)
    return doc


# ID 表示专题id
def updateById(id, filedata={}):
    assert id
    update_field = {}
    for filename in filedata:
        update_field['Document.' + filename] = filedata[filename]
    res = models.DocumentInformation.objects.filter(uuid=id).update(update_field)
    return res


# 更新专题多媒体文件
def updateURLById(id, medias={}):
    assert id
    res = models.DocumentInformation.objects.filter(uuid=id).update(included_media=medias)
    return res


# ID 表示专题id not专题uuid
def deleteById(id):
    assert id
    res = models.DocumentInformation.objects.filter(id=id).delete()
    return res
