from typing import ClassVar, Optional

import attr


@attr.s(auto_attribs=True)
class AppConfig:
    TIMER_VALUE: ClassVar[str] = "timerValue"
    SNOOZE_HOURS: ClassVar[str] = "snoozeHours"
    timer_value: Optional[int] = 25
    snooze_hours: Optional[int] = 6
