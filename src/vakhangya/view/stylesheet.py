APP_STYLESHEET = '''

* {
    icon-size: 20px;
}

QFrame[curve-cornered] {
    border: 1px solid black;
    border-radius: 6px;
}

QToolTip {
    border: 0px;
}

QPushButton {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
    border: 2px solid #8f8f91;
    border-radius: 6px;
    padding: 2px;
}

QPushButton:hover {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #c3c4c7, stop: 1 #f6f7fa);
}

QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #d7d8db, stop: 1 #f6f7fa);
    border: 2px solid darkGrey;
}

QPushButton:checked {
    background-color: lightgrey;
}

QPushButton:disabled {
    opacity: 0.65;
}

'''
