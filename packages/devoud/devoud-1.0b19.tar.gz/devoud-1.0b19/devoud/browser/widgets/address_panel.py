from devoud.browser import *
from devoud.browser.web.search_engines import *
from devoud.browser.context_menu import BrowserContextMenu


class AddressPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.FS = self.window().FS
        self.tab_widget = self.window().tab_widget
        self.setObjectName("address_panel")
        self.setMinimumSize(QSize(550, 45))
        self.setMaximumSize(QSize(16777215, 45))
        self.setLayout(QHBoxLayout())

        # кнопки на панели
        self.add_tab_button = self.PanelButton(self, './ui/custom/svg/add.svg', self.tab_widget.create_tab)
        self.add_tab_button.setObjectName('add_tab_button_panel')
        self.add_tab_button.hide()
        self.back_button = self.PanelButton(self, './ui/custom/svg/arrow_left.svg', self.window().back_page)
        self.back_button.setObjectName('back_button')
        self.forward_button = self.PanelButton(self, './ui/custom/svg/arrow_right.svg', self.window().forward_page)
        self.forward_button.setObjectName('forward_button')
        self.stop_load_button = self.PanelButton(self, './ui/custom/svg/close(address_panel).svg', self.window().stop_load_page)
        self.stop_load_button.setObjectName('stop_load_button')
        self.stop_load_button.hide()
        self.update_button = self.PanelButton(self, './ui/custom/svg/update.svg', self.window().update_page)
        self.update_button.setObjectName('update_button')
        self.home_button = self.PanelButton(self, './ui/custom/svg/home.svg', lambda: self.window().load_home_page(new_tab=False))
        self.home_button.setObjectName('home_button')

        # адресная строка
        self.address_line_frame = QFrame(self)
        self.address_line_frame.setObjectName("address_line_frame")
        self.address_line_frame.setFixedHeight(29)
        self.address_line_frame.setLayout(QHBoxLayout())
        self.address_line_frame.layout().setSpacing(0)
        self.address_line_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.address_line_frame)

        self.search_box = QComboBox(self)
        [self.search_box.addItem(QIcon(search_engines[key][2]), key) for key in search_engines.keys()]
        self.search_box.setObjectName("search_box")
        self.search_box.setFixedSize(QSize(115, 29))
        self.address_line_frame.layout().addWidget(self.search_box)
        self.search_box.setCurrentText(self.FS.get_option('searchEngine'))

        self.address_line_edit = self.AddressLineEdit(self)
        self.address_line_frame.layout().addWidget(self.address_line_edit)

        self.bookmark_button = self.PanelButton(self.address_line_frame, './ui/custom/svg/bookmark_empty.svg', self.window().add_bookmark)
        self.bookmark_button.setObjectName('bookmark_button')

        # контекстное меню для вызова панели управления
        self.menu_button = self.PanelButton(self, './ui/custom/svg/options.svg')
        self.menu_button.setObjectName('menu_button')
        self.options_menu = BrowserContextMenu(self)
        self.options_menu.setFixedWidth(100)
        self.options_menu.setAttribute(Qt.WA_TranslucentBackground)
        self.options_menu.addAction('Настройки', lambda: self.tab_widget.create_tab('devoud://control#settings'))
        self.options_menu.addAction('История', lambda: self.tab_widget.create_tab('devoud://control#history'))
        self.options_menu.addAction('Закладки', lambda: self.tab_widget.create_tab('devoud://control#bookmarks'))
        self.options_menu.addAction('Загрузки', lambda: self.tab_widget.create_tab('devoud://control#downloads'))
        self.menu_button.setMenu(self.options_menu)

    class AddressLineEdit(QLineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setObjectName("address_line_edit")
            self.setPlaceholderText('Поиск или ссылка')
            self.setFixedHeight(29)
            self.setCursor(QCursor(Qt.PointingHandCursor))
            self.setClearButtonEnabled(True)
            self.returnPressed.connect(self.load_from_line)

        def load_from_line(self):
            self.window().tab_widget.current().load(self.text(), allow_search=True)
            self.clearFocus()

        def focusOutEvent(self, event):
            self.setCursorPosition(0)
            super().focusOutEvent(event)

    class PanelButton(QPushButton):
        def __init__(self, parent=None, icon=None, command=None):
            super().__init__(parent)
            self.setObjectName("address_panel_button")
            self.setFixedSize(QSize(30, 29))
            self.setCursor(QCursor(Qt.PointingHandCursor))

            if command is not None:
                self.clicked.connect(command)

            if icon is not None:
                self.icon = icon
                self.setIcon(QIcon(icon))
                self.setIconSize(QSize(25, 19))

            if parent is not None:
                parent.layout().addWidget(self)
