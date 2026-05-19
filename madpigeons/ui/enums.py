from enum import Enum


class HorizontalAlignment(Enum):
    Left = "left"
    Center = "center"
    Right = "right"


class VerticalAlignment(Enum):
    Top = "top"
    Center = "center"
    Bottom = "bottom"


class UIState(Enum):
    Idle = "idle"
    Hover = "hover"
    Press = "press"
