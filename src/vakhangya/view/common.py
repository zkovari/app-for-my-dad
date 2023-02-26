import qtawesome
from PySide6.QtGui import QIcon


def qta_icon(name: str, color: str = 'black', color_on: str = 'black') -> QIcon:
    if name.startswith('md') or name.startswith('ri'):
        return qtawesome.icon(name, options=[{'scale_factor': 1.2}], color=color, color_on=color_on)
    return qtawesome.icon(name, color=color, color_on=color_on)
