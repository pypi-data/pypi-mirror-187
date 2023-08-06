from devoud.browser import *


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("title_bar")

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setObjectName("title_label")
        self.layout.addWidget(self.label)

        self.window_buttons_widget = QWidget(self)
        self.window_buttons_widget.setFixedWidth(80)
        self.window_buttons_widget.setObjectName("window_buttons")
        self.window_buttons_layout = QHBoxLayout(self.window_buttons_widget)
        self.window_buttons_layout.setContentsMargins(0, 5, 0, 0)

        self.hide_button = QPushButton(self)
        self.hide_button.setObjectName("hide_button")
        self.hide_button.setFixedSize(QSize(23, 23))
        self.hide_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.hide_button.setFlat(True)
        self.window_buttons_layout.addWidget(self.hide_button)

        self.maximize_button = QPushButton(self)
        self.maximize_button.setObjectName("maximize_button")
        self.maximize_button.setFixedSize(QSize(23, 23))
        self.maximize_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.maximize_button.setFlat(True)
        self.window_buttons_layout.addWidget(self.maximize_button)

        self.close_button = QPushButton(self)
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(QSize(23, 23))
        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_button.setFlat(True)
        self.window_buttons_layout.addWidget(self.close_button)

        self.right_spacer = QSpacerItem(11, 10)

        self.layout.addWidget(self.window_buttons_widget)
        self.layout.addItem(self.right_spacer)

    def mouseDoubleClickEvent(self, event):
        self.window().restore_or_maximize()
