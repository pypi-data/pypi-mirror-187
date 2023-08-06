from devoud.browser import *
from devoud.browser.styles.theme import Theme
from devoud.browser.web.search_engines import search_engines
from devoud.browser.widgets.address_panel import AddressPanel
from devoud.browser.filesystem import FileSystem
from devoud.browser.widgets.find_on_page import FindWidget
from devoud.browser.download_manager import DownloadManager
from devoud.browser.pages.observer import PagesObserver
from devoud.browser.widgets.tab_widget import BrowserTabWidget
from devoud.browser.widgets.title_bar import TitleBar
import devoud


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.FS = FileSystem()

        self.new_page_dict = {'Заставка с часами': lambda: 'https://web.tabliss.io/',
                              'Поисковик': lambda: search_engines[self.FS.get_option('searchEngine')][1],
                              'Домашняя страница': lambda: QUrl.fromUserInput(
                                  self.FS.get_option('homePage')).toString()}

        self.new_page = self.new_page_dict.get(self.FS.get_option('newPage'))()
        self.systemFrame = self.FS.get_option('systemWindowFrame')

        self.theme = Theme(self)
        self.setWindowIcon(QIcon('./ui/svg/browser_icon.svg'))
        self.setWindowTitle(__name__)
        self.setMinimumSize(QSize(400, 300))

        # профиль для веб-страниц
        self.profile = QWebEngineProfile('DevoudProfile')
        self.profile.setCachePath(str(self.FS.local_path_config.parent))
        self.download_manager = DownloadManager(self)
        self.profile.downloadRequested.connect(lambda req: self.download_manager.download_requested(req))

        # шрифт
        QFontDatabase.addApplicationFont("./ui/fonts/ClearSans-Medium.ttf")
        self.setFont(QFont('Clear Sans Medium'))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.window_layout = QGridLayout(self.central_widget)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # для растяжения окна с кастомной рамкой
        self.size_grip_right = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_right, 1, 2)
        self.size_grip_right.setFixedWidth(5)
        self.size_grip_right.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.size_grip_right.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_left = QSizeGrip(self)
        self.size_grip_left.setFixedWidth(5)
        self.size_grip_left.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.window_layout.addWidget(self.size_grip_left, 1, 0)
        self.size_grip_left.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_top = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_top, 0, 1)
        self.size_grip_top.setFixedHeight(5)
        self.size_grip_top.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.size_grip_top.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_bottom = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_bottom, 2, 1)
        self.size_grip_bottom.setFixedHeight(5)
        self.size_grip_bottom.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.size_grip_bottom.setStyleSheet('border-radius: 5px; background: transparent;')

        # все кроме size grip
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName('main_frame')

        # ломается рендер веб-страниц
        # self.window_shadow = QGraphicsDropShadowEffect(self)
        # self.window_shadow.setBlurRadius(17)
        # self.window_shadow.setXOffset(0)
        # self.window_shadow.setYOffset(0)
        # self.window_shadow.setColor(QColor(0, 0, 0, 150))
        # self.main_frame.setGraphicsEffect(self.window_shadow)

        self.window_layout.addWidget(self.main_frame, 1, 1)
        self.main_layout = QGridLayout(self.main_frame)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # адресная панель
        self.address_panel = AddressPanel(self)
        self.main_layout.addWidget(self.address_panel, 1, 0, 1, 1)
        self.address_line_edit = self.address_panel.address_line_edit
        self.bookmark_button = self.address_panel.bookmark_button
        self.add_tab_button = self.address_panel.add_tab_button
        self.bookmarks_state = False

        # виджет вкладок
        self.main_layout.addWidget(self.tab_widget, 3, 0)
        self.tab_widget.set_tab_bar_position()

        # кастомная рамка окна
        self.title_bar = TitleBar(self)
        self.main_layout.addWidget(self.title_bar, 0, 0)
        self.title_bar.close_button.clicked.connect(self.close)
        self.title_bar.maximize_button.clicked.connect(self.restore_or_maximize)
        self.title_bar.hide_button.clicked.connect(self.showMinimized)

        def move_window(event):
            if self.isMaximized():
                self.restore_or_maximize()
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.title_bar.mouseMoveEvent = move_window

        # выбор рамки окна
        if not self.systemFrame:
            # убрать системную рамку окна
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.window_corner_radius('12px')
        else:
            self.title_bar.deleteLater()
            self.size_grip_right.deleteLater()
            self.size_grip_left.deleteLater()
            self.size_grip_top.deleteLater()
            self.size_grip_bottom.deleteLater()

        # комбинации клавиш
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.update_page)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_find_on_page)
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(lambda: self.tab_widget.create_tab(self.new_page))
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(
            lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))

        # восстановление предыдущей сессии
        self.restore_or_home()

    def change_style(self, name=None):
        self.theme = Theme(self, name)
        self.setStyleSheet(self.theme.style())
        self.address_line_edit.findChild(QToolButton).setIcon(QIcon("./ui/custom/svg/close(address_line_frame).svg"))
        self.check_state_bookmark()

    def window_corner_radius(self, radius):
        self.main_frame.setStyleSheet(Template("""
        #main_frame { 
            border-radius: $radius;
        }""").substitute(radius=radius))

    def show_find_on_page(self):
        page = self.tab_widget.current()
        page_find_widget = page.findChild(FindWidget)
        if page_find_widget:
            if not page_find_widget.isHidden():
                page_find_widget.hide_find()
            else:
                page_find_widget.show()
                page_find_widget.find_focus()
                page_find_widget.find_text()
        elif not page.view.embedded:
            find_widget = FindWidget(page)
            page.layout().addWidget(find_widget)
            find_widget.show()
            find_widget.find_focus()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def restore_or_maximize(self):
        if self.isMaximized():
            self.window_corner_radius('12px')
            self.showNormal()
        else:
            self.window_corner_radius('0px')
            self.showMaximized()

    def load_home_page(self, new_tab=True):
        if new_tab:
            self.tab_widget.create_tab()
        self.tab_widget.current().load(self.FS.get_option('homePage'))

    def restore_or_home(self):
        if self.FS.get_option('restoreTabs'):
            with open(f'{self.FS.config_dir()}/tabs') as tabs_file:
                links = tabs_file.read().splitlines()
                if not links:
                    return self.load_home_page()

            for link in range(len(links) - 1):
                self.tab_widget.create_tab(links[link])
            self.tab_widget.setCurrentIndex(int(links[-1]))  # последняя посещенная вкладка
        else:
            self.load_home_page()

    def set_title(self, text):
        self.setWindowTitle(f"{text} – {devoud.__name__} {devoud.__version__}")
        if not self.systemFrame:
            self.title_bar.label.setText(f"{text} – {devoud.__name__} {devoud.__version__}")

    def back_page(self):
        self.tab_widget.current().back()

    def forward_page(self):
        self.tab_widget.current().forward()

    def stop_load_page(self):
        self.tab_widget.current().stop()

    def update_page(self):
        self.tab_widget.current().reload()

    def check_state_bookmark(self):
        with open(f'{self.FS.config_dir()}/bookmarks', 'r') as bookmarks_file:
            bookmarks = bookmarks_file.read().splitlines()
            self.bookmarks_state = self.address_line_edit.text() in bookmarks
            self.bookmark_button.setStyleSheet(
                f"icon: url(./ui/custom/svg/{'bookmark' if self.bookmarks_state else 'bookmark_empty'}.svg);")

    def add_bookmark(self):
        link = self.address_line_edit.text()
        with open(f'{self.FS.config_dir()}/bookmarks', 'r') as bookmarks_file:
            bookmarks = bookmarks_file.read().splitlines()
            if link in bookmarks:
                bookmarks.remove(link)
            else:
                bookmarks.append(link)
        with open(f'{self.FS.config_dir()}/bookmarks', 'w') as bookmarks_file:
            bookmarks = '\n'.join(bookmarks)
            bookmarks_file.write(bookmarks)
        self.check_state_bookmark()
        PagesObserver.control_update_lists()

    def save_session(self):
        if self.FS.get_option('restoreTabs'):
            with open(f'{self.FS.config_dir()}/tabs', 'w') as tabs_file:
                tabs = []
                for tab_index in range(self.tab_widget.count()):
                    tabs.append(self.tab_widget.widget(tab_index).url)
                tabs.append(str(self.tab_widget.currentIndex()))  # последняя посещенная вкладка
                tabs = '\n'.join(tabs)
                tabs_file.write(tabs)
            print('[Вкладки]: Текущая сессия сохранена')

    def closeEvent(self, event):
        self.save_session()
        for page in PagesObserver.pages():
            page.deleteLater()

    def restart(self):
        self.save_session()
        os.execv(sys.executable, ['python'] + sys.argv)

    @cached_property
    def tab_widget(self):
        return BrowserTabWidget()
