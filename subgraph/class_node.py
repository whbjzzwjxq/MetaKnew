import json
from datetime import datetime, timezone
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from es_module.logic_class import bulk_add_node_index
from record.logic_class import error_check
from record.models import WarnRecord, NodeVersionRecord
from subgraph.class_media import BaseMedia
from subgraph.models import NodeCtrl, MediaCtrl
from tools import base_tools
from tools.base_tools import neo4j_create_node


class BaseNode(base_tools.BaseModel):

    def __init__(self, _id: int, user_id: int, _type='node', collector=base_tools.NeoSet()):

        # 以下是模型
        super().__init__(_id, user_id, _type, collector)
        self.type = _type
        self.warn: Optional[WarnRecord] = None
        self.loading_history: Optional[NodeVersionRecord] = None
        self.history = NodeVersionRecord.objects.none()

    # ----------------- query ----------------

    def query_all(self):
        """
        查询所有内容 包括Neo4j节点 翻译 历史文件
        :return:
        """
        success = self.query_base()
        if success:
            self.query_node()
            self.query_history()
        return self

    def query_with_label(self, p_label):
        """
        带有主标签的查询
        :param p_label:
        :return:
        """
        ctrl_set = NodeCtrl.objects.filter(PrimaryLabel=p_label)
        try:
            self.ctrl = ctrl_set.objects.get(pk=self.id)
            self.p_label = self.ctrl.PrimaryLabel
            self.__query_info()
            return self
        except ObjectDoesNotExist:
            return None

    def query_history(self):
        self.history = NodeVersionRecord.objects.filter(SourceId=self.id)
        if len(self.history) == 0:
            self.lack.append("history")

    # ---------------- create ----------------
    # @error_check
    def create(self, data):
        self.is_draft = False
        self.is_create = True
        assert "Name" in data
        assert "PrimaryLabel" in data
        self.p_label = data["PrimaryLabel"]
        self.__history_create(data=data)  # done 09-05

        self.__ctrl_create(data=data)  # done 09-10
        self.__info_create(data=data)  # done 09-10
        self.name_checker()  # done 09-13
        self.auth_create(data=data)  # done 09-10
        props = {
            "Name": data["Name"],
            "Imp": data["BaseImp"],
            "HardLevel": data["BaseHardLevel"]
        }
        self.node = neo4j_create_node(
            labels=data["Labels"] + data["Topic"],
            _id=self.id,
            _type=self.type,
            plabel=self.p_label,
            props=props,
            is_user_made=self.is_user_made,
            is_common=data["$_IsCommon"],
            collector=self.collector)
        self.collector.tx.create(self.node)
        return self

    # ---------------- __private_create ----------------
    def __info_create(self, data):
        """
        info创建过程
        :param data:
        :return:
        """
        # 初始化
        self.info = base_tools.node_init(self.p_label)()
        self.info.NodeId = self.id
        self.info.PrimaryLabel = self.p_label
        if type(data["MainPic"]) == str and data["MainPic"] != " ":
            self.main_pic_setter(data["MainPic"])
        if data["IncludedMedia"]:
            self.media_setter(data["IncludedMedia"])

        # update其他数据
        self.info_update(data)
        return self

    # 设置控制信息 done
    def __ctrl_create(self, data):
        if self.is_user_made:
            contributor = {"create": "system", "update": []}
        else:
            contributor = {"create": "", "update": []}
        self.ctrl = NodeCtrl(
            NodeId=self.id,
            CountCacheTime=datetime.now(tz=timezone.utc).replace(microsecond=0),
            Is_UserMade=self.is_user_made,
            CreateUser=self.user_id,
            PrimaryLabel=self.p_label,
            Contributor=contributor
        )

    def __history_create(self, data):
        if self.is_create:
            version_id = 1
        else:
            self.query_history()
            version_id = self.history.aggregate(Max("VersionId"))
            version_id += 1
        self.loading_history = NodeVersionRecord(VersionId=version_id,
                                                 SourceId=self.id,
                                                 SourceType=self.p_label,
                                                 CreateUser=self.user_id,
                                                 Name=data["Name"],
                                                 Content=data,
                                                 Is_Draft=self.is_draft
                                                 )

    def name_checker(self):
        """
        查询是否有类似名字的节点
        :return:
        """
        similar_node = base_tools.node_init(self.p_label).objects.filter(Name=self.info.Name)
        if len(similar_node) > 0:
            warn = {"field": "Name",
                    "warn_type": "similar_node_id" + json.dumps([node.NodeId for node in similar_node])}
            self.warn.WarnContent.append(warn)

    def main_pic_setter(self, media_name):
        media_manager = BaseMedia.oss_manager
        if media_manager.object_exists(media_name):
            self.info.MainPic = media_name
        else:
            warn = {"field": "MainPic", "warn_type": "empty_prop"}
            self.warn.WarnContent.append(warn)
        return self

    def media_setter(self, media_list):
        for media_id in media_list:
            try:
                record = MediaCtrl.objects.get(pk=media_id)
                if record:
                    self.info.IncludedMedia.append(media_id)
            except ObjectDoesNotExist:
                pass
        return self

    def delete(self):
        # todo 节点删除 level: 2
        pass

    def merge(self, node1):
        # todo 节点merge level: 2
        pass

    def change_plabel(self):
        pass
        # todo 改变主标签 level: 2

    def save(self):
        """
        注意尽量不要使用单个Node保存
        :return:
        """
        self.ctrl.save()
        self.info.save()
        if self.authority:
            self.authority.save()
        if self.loading_history:
            self.loading_history.save()
        if self.warn:
            self.warn.save()
        bulk_add_node_index([self])

    def node_index(self):
        ctrl = self.ctrl
        info = self.info
        body = {
            "id": self.id,
            "type": self.type,
            "CreateUser": ctrl.CreateUser,
            "UpdateTime": ctrl.UpdateTime,
            "Language": info.Language,
            "MainPic": info.MainPic,
            "Name": {
                "zh": "",
                "en": "",
                "auto": info.Name
            },
            "Tags": {
                "PrimaryLabel": info.PrimaryLabel,
                "Alias": info.Alias,
                "Labels": info.Labels,
                "Topic": info.Topic
            },
            "Level": {
                "Imp": ctrl.Imp,
                "HardLevel": ctrl.HardLevel,
                "Useful": ctrl.Useful,
                "Star": ctrl.Star,
                "Hot": ctrl.Hot,
                "TotalTime": ctrl.TotalTime
            }
        }
        for lang in body["Name"]:
            if lang in info.Translate:
                body["Name"][lang] = info.Translate[lang]

        return body

    def output_table_create(self):
        return self.ctrl, self.info, self.authority, self.warn, self.loading_history
