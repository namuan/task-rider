from typing import ClassVar, Optional

import attr


@attr.s(auto_attribs=True)
class AppConfig:
    TIMER_VALUE: ClassVar[str] = "timerValue"
    timer_value: Optional[int] = 25
