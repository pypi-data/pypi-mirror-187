import io
from typing import Any, Callable, Dict, List, Literal, Tuple

Key = Literal[
    'mouse1', 'mouse2', 'mouse3', 'tab', 'left_arrow', 'right_arrow', 'up_arrow', 'down_arrow', 'pageup', 'pagedown',
    'home', 'end', 'insert', 'delete', 'backspace', 'space', 'enter', 'escape', 'apostrophe', 'comma', 'minus',
    'period', 'slash', 'semicolon', 'equal', 'left_bracket', 'backslash', 'right_bracket', 'graveaccent', 'capslock',
    'scrolllock', 'numlock', 'printscreen', 'pause', 'keypad_0', 'keypad_1', 'keypad_2', 'keypad_3', 'keypad_4',
    'keypad_5', 'keypad_6', 'keypad_7', 'keypad_8', 'keypad_9', 'keypad_decimal', 'keypad_divide', 'keypad_multiply',
    'keypad_subtract', 'keypad_add', 'keypad_enter', 'left_shift', 'left_ctrl', 'left_alt', 'left_super',
    'right_shift', 'right_ctrl', 'right_alt', 'right_super', 'menu', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
]


class MainWindow:
    size: Tuple[int, int]
    ratio: float
    mouse: Tuple[int, int]
    mouse_delta: Tuple[int, int]
    mouse_wheel: int
    frame: int
    text: str
    log: io.StringIO
    config: Dict[str, Any]

    def key_pressed(self, key: Key) -> bool: ...
    def key_released(self, key: Key) -> bool: ...
    def key_down(self, key: Key) -> bool: ...
    def key_up(self, key: Key) -> bool: ...
    def image(self, name: str, texture: int, position: Tuple[float, float], size: Tuple[float, float], flip: bool = False) -> None: ...
    def slider(self, name: str, value: float = 0.0, min: float = -1.0, max: float = 1.0, format: str = '%.2f') -> None: ...
    def increment(self, name: str, value: int = 0, min: int = 0, max: int = 0) -> None: ...
    def checkbox(self, name: str, value: bool = False) -> None: ...
    def combo(self, name: str, value: str, options: List[str]) -> None: ...
    def button(self, name: str, click: Callable) -> None: ...
    def tooltip(self, text: str) -> None: ...
    def group(self, name: str) -> None: ...
    def update(self) -> None: ...


def main_window(size: Tuple[int, int] = ..., title: str = 'Mollia Window') -> MainWindow: ...


wnd: MainWindow
keys: Dict[str, int]
