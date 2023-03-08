import textwrap
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolButton, QLabel, QFrame, QWidget, QScrollArea, QLineEdit, QSizePolicy
from qtanim import fade_in
from qthandy import transparent, hbox, spacer, incr_font, margins, vbox, vspacer, clear_layout

from vakhangya.view.common import qta_icon
from vakhangya.view.domain import Album, Song


class Icon(QToolButton):
    def __init__(self, iconName: str, parent=None):
        super().__init__(parent)
        transparent(self)
        self.setIcon(qta_icon(iconName))


class SongWidget(QWidget):
    def __init__(self, song: Song, parent=None):
        super().__init__(parent)
        self._song = song

        hbox(self)
        self._lineTitle = QLineEdit(self)
        self._lineTitle.setText(self._song.title)
        self._lineTitle.setReadOnly(True)
        self.layout().addWidget(self._lineTitle)


class SongsEditor(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._centralWidget = QWidget(self)
        self._centralWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWidget(self._centralWidget)
        vbox(self._centralWidget, spacing=3)
        margins(self._centralWidget, left=15, right=15)

        self._centralWidget.layout().addWidget(vspacer())

    def setSongs(self, songs: List[Song]):
        self.clear()

        for song in songs:
            wdg = SongWidget(song)
            self._centralWidget.layout().addWidget(wdg)
            fade_in(wdg)

        self._centralWidget.layout().addWidget(vspacer())

    def clear(self):
        clear_layout(self._centralWidget)


class AlbumHeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        hbox(self, spacing=2)
        margins(self, left=5)

        self._bandIcon = Icon('fa5s.guitar')
        self._yearIcon = Icon('fa5.calendar-alt')
        self._albumIcon = Icon('mdi.album')

        self._lblBand = QLabel()
        self._lblYear = QLabel()
        self._lblAlbum = QLabel()
        for lbl in self._labels():
            incr_font(lbl, 2)
            lbl.setHidden(True)

        self.layout().addWidget(self._bandIcon)
        self.layout().addWidget(self._lblBand)
        self.layout().addWidget(self._yearIcon)
        self.layout().addWidget(self._lblYear)
        self.layout().addWidget(self._albumIcon)
        self.layout().addWidget(self._lblAlbum)
        self.layout().addWidget(spacer())

    def setAlbum(self, album: Album):
        self._lblAlbum.setText(textwrap.shorten(album.album, width=50))
        self._lblAlbum.setToolTip(album.album)
        self._lblYear.setText(str(album.year))
        self._lblYear.setToolTip(str(album.year))
        self._lblBand.setText(textwrap.shorten(album.band, width=50))
        self._lblBand.setToolTip(album.band)
        for lbl in self._labels():
            fade_in(lbl)

    def clear(self):
        for lbl in self._labels():
            lbl.clear()
            lbl.setToolTip('')
            lbl.setHidden(True)

    def _labels(self) -> List[QLabel]:
        return [self._lblAlbum, self._lblYear, self._lblBand]


class AlbumDisplayWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty('curve-cornered', True)

        self._header = AlbumHeaderWidget()
        self._songsContainer = SongsEditor()

        vbox(self)
        self.layout().addWidget(self._header)
        self.layout().addWidget(self._songsContainer)

    def clear(self):
        self._header.clear()
        self._songsContainer.clear()

    def setAlbum(self, album: Album):
        self._header.setAlbum(album)
        self._songsContainer.setVisible(True)
        self._songsContainer.setSongs(album.songs)
