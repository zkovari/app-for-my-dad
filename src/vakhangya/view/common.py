import qtawesome
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtWidgets import QApplication, QMessageBox


def qta_icon(name: str, color: str = 'black', color_on: str = 'black') -> QIcon:
    if name.startswith('md') or name.startswith('ri'):
        return qtawesome.icon(name, options=[{'scale_factor': 1.2}], color=color, color_on=color_on)
    return qtawesome.icon(name, color=color, color_on=color_on)


def error_msg(message: str, parent=None):
    QApplication.setOverrideCursor(QCursor(Qt.CursorShape.ArrowCursor))
    QMessageBox.critical(parent, 'Error', message)
    QApplication.restoreOverrideCursor()
