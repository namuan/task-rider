import logging

import dataset

from app.core.str_utils import plain_to_b64_str, b64_to_plain_str
from app.data.entities import (
    AppState,
    APP_STATE_RECORD_TYPE,
    TASK_ENTITY_RECORD_TYPE,
    TaskEntity, )
from app.events.signals import AppEvents


class LiteDataStore:
    app_events = AppEvents()

    def __init__(self, data_dir):
        self.data_dir = data_dir
        db_path = f"sqlite:///{self.data_dir}/app.db"
        self.db = dataset.connect(db_path)
        self._app_state = self.get_app_state()

    @property
    def app_state(self):
        return self._app_state

    def update_app_state_in_db(self):
        app_state_table = self.db[self.app_state.record_type]
        app_state_table.upsert(
            dict(name=self.app_state.record_type, object=self.app_state.to_json_str()),
            ["name"],
        )

    def get_app_state(self):
        table = self.db[APP_STATE_RECORD_TYPE]
        app_state_record = table.find_one(name=APP_STATE_RECORD_TYPE)
        if not app_state_record:
            return AppState()

        return AppState.from_json_str(app_state_record["object"])

    def update_scratch_note(self, scratch_note):
        logging.debug("Updating Scratch Pad: Characters: {}".format(len(scratch_note)))
        if not scratch_note:
            return

        self.app_state.scratch_note = plain_to_b64_str(scratch_note)
        self.update_app_state_in_db()

    def get_scratch_note(self):
        return b64_to_plain_str(self.app_state.scratch_note)

    def update_task(self, task_entity):
        table = self.db[TASK_ENTITY_RECORD_TYPE]
        table.upsert(
            dict(
                name=TASK_ENTITY_RECORD_TYPE,
                task_id=task_entity.id,
                task_state=str(task_entity.task_state),
                object=task_entity.to_json_str(),
            ),
            ["task_id"],
        )
        self.app_events.task_updated.emit(task_entity.id)

    def get_task_entity(self, task_id):
        table = self.db[TASK_ENTITY_RECORD_TYPE]
        entity = table.find_one(task_id=task_id)
        return TaskEntity.from_json_str(entity["object"])

    def get_tasks(self, task_state):
        table = self.db[TASK_ENTITY_RECORD_TYPE]
        new_tasks = table.find(name=TASK_ENTITY_RECORD_TYPE, task_state=task_state)
        step_entities = [
            TaskEntity.from_json_str(task["object"]) for task in new_tasks
        ]
        return sorted(step_entities, key=lambda s: s.order or 0,)
