import logging
from datetime import datetime


class TimeReportController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # app events
        self.app.data.app_events.timer_started.connect(self.log_start_time)
        self.app.data.app_events.timer_paused.connect(self.log_stop_time)

    def log_start_time(self):
        task_entity = self.app.data.get_top_task()
        task_title = getattr(task_entity, "task_title", "") if task_entity else ""
        reminder_id = getattr(task_entity, "reminder_id", "") if task_entity else ""
        started_at = datetime.now().isoformat()
        logging.info(
            'timer_start task_title="%s" reminder_id="%s" started_at="%s"',
            self._escape_log_str(task_title),
            self._escape_log_str(reminder_id),
            started_at,
        )

    def log_stop_time(self):
        task_entity = self.app.data.get_top_task()
        task_title = getattr(task_entity, "task_title", "") if task_entity else ""
        reminder_id = getattr(task_entity, "reminder_id", "") if task_entity else ""
        stopped_at = datetime.now().isoformat()
        logging.info(
            'timer_stop task_title="%s" reminder_id="%s" stopped_at="%s"',
            self._escape_log_str(task_title),
            self._escape_log_str(reminder_id),
            stopped_at,
        )

    def _escape_log_str(self, value: object) -> str:
        if value is None:
            return ""
        s = str(value)
        return s.replace("\\", "\\\\").replace('"', '\\"')
