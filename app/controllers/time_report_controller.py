import logging
from datetime import datetime

from app.data.entities import TimeReportEntity
from app.utils.uuid_utils import gen_uuid


class TimeReportController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # app events
        self.app.data.app_events.timer_started.connect(self.log_start_time)
        self.app.data.app_events.timer_paused.connect(self.log_stop_time)

    def log_start_time(self):
        task_entity = self.app.data.get_top_task()
        logging.info("Logging start time for task : {}".format(task_entity))
        time_report: TimeReportEntity = TimeReportEntity(
            report_id=gen_uuid(),
            task_id=task_entity.id,
            task_title=task_entity.task_title,
            timer_start=datetime.now()
        )
        self.app.data.update_time_report(time_report)

    def log_stop_time(self):
        task_entity = self.app.data.get_top_task()
        logging.info("Logging end time for task : {}".format(task_entity))
        time_report: TimeReportEntity = TimeReportEntity(
            report_id=gen_uuid(),
            task_id=task_entity.id,
            task_title=task_entity.task_title,
            timer_stop=datetime.now()
        )
        self.app.data.update_time_report(time_report)
