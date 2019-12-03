from __future__ import annotations

import enum
import re
from functools import reduce
from typing import Optional
from typing import overload


class Colors(enum.Enum):
    RESET = '\033[0m'
    BOLD = '\033[01m'
    RED = '\033[31m'
    RED_BG = '\033[41m'
    GREEN = '\033[32m'
    GREEN_BG = '\033[42m'
    YELLOW = '\033[33m'
    YELLOW_BG = '\033[43m'
    BLUE = '\033[34m'
    BLUE_BG = '\033[44m'
    MAGENTA = '\033[35m'
    MAGENTA_BG = '\033[45m'
    CYAN = '\033[36m'
    CYAN_BG = '\033[46m'
    WHITE = '\033[37m'
    WHITE_BG = '\033[47m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_BLACK_BG = '\033[100m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_RED_BG = '\033[101m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_GREEN_BG = '\033[102m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_YELLOW_BG = '\033[103m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_BLUE_BG = '\033[104m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_MAGENTA_BG = '\033[105m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_CYAN_BG = '\033[106m'
    BRIGHT_WHITE = '\033[97m'
    BRIGHT_WHITE_BG = '\033[107m'

    @overload
    def __call__(self, string: None) -> None:
        ...

    @overload
    def __call__(self, string: str) -> str:
        ...

    def __call__(self, string: Optional[str]):
        if string is None:
            return None
        return re.sub(r'^(\s*)(.*)(\s*)$', r'\1%s\2%s\3' % (self.value, Colors.RESET.value), string, flags=re.MULTILINE)

    @classmethod
    def apply(cls, string: str, *colors: Colors) -> str:
        return reduce(lambda s, color: color(s), colors, string)