from record.models import WarnRecord, SourceAddRecord


class IdGenerationError(BaseException):
    pass


class ObjectAlreadyExist(BaseException):
    pass


class UnAuthorizationError(BaseException):
    pass


class RewriteMethodError(BaseException):
    pass


def field_check(_func):
    def wrapped(self, field, new_prop, old_prop):
        if isinstance(new_prop, str) and len(new_prop) > 1024:
            self.warn.WarnContent.append({"field": field.name, "warn_type": "toolong_str"})

        if isinstance(new_prop, list) and len(new_prop) > 128:
            self.warn.WarnContent.append({"field": field.name, "warn_type": "toolong_list"})

        if isinstance(new_prop, dict) and len(new_prop) > 128:
            self.warn.WarnContent.append({"field": field.name, "warn_type": "toolong_dict"})

        if not bool(new_prop):
            self.warn.WarnContent.append({"field": field.name, "warn_type": "empty_prop"})

        # 这里主要是针对JSONField 和 ArrayField
        if type(new_prop) != type(old_prop):
            self.warn.WarnContent.append({"field": field.name, "warn_type": "error_type"})
        return _func(self, field, new_prop, old_prop)

    return wrapped


class EWRecord:

    def __init__(self):
        self.record = SourceAddRecord.objects.all()

    def query_by_criteria(self, criteria_query):
        assert criteria_query["source_type"] == "AddRecord"
        if criteria_query["labels"] is not []:
            for label in criteria_query["labels"]:
                self.query_by_status(label)

        if criteria_query["props"] is not {}:
            for key, value in criteria_query["props"].items():
                self.query_by_props(key=key, value=value)
        limit = criteria_query["limit"]
        return self.record[:limit]

    def query_by_status(self, label):
        self.record = self.record.filter({label: True})
        return self

    def query_by_props(self, key, value):
        self.record = self.record.filter({key: value})
        return self

    @staticmethod
    def add_warn_record(user, source_id, source_label, content):
        record = WarnRecord(
            SourceId=source_id,
            SourceLabel=source_label,
            CreateUser=user,
            WarnContent=content
        )
        return record

    @staticmethod
    def bulk_save_warn_record(records):
        result = WarnRecord.objects.bulk_create(records)
        return result
