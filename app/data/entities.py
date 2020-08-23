import json
from datetime import datetime
from enum import Enum

import attr
import cattr

APP_STATE_RECORD_TYPE = "app_state"
TASK_ENTITY_RECORD_TYPE = "task_entity"


class BaseEntity:
    @classmethod
    def from_json_str(cls, json_str):
        json_obj = json.loads(json_str)
        return cls.from_json(json_obj)

    @classmethod
    def from_json(cls, json_obj):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)

    def to_json_str(self):
        return json.dumps(self.to_json())


@attr.s(auto_attribs=True)
class AppState(BaseEntity):
    record_type: str = APP_STATE_RECORD_TYPE
    scratch_note: str = ""


class TaskState(Enum):
    NEW = "new"
    DONE = "done"


@attr.s(auto_attribs=True)
class TaskEntity(BaseEntity):
    id: str
    task_title: str
    order: int = 0
    added_time = datetime.now()
    done_time = None
    record_type: str = TASK_ENTITY_RECORD_TYPE
    task_state: TaskState = TaskState.NEW

    def mark_as_done(self):
        self.task_state = TaskState.DONE
        self.done_time = datetime.now()