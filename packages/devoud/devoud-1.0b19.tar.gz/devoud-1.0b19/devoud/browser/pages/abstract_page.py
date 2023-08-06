from devoud.browser import *
from devoud.browser.pages import *
from devoud.browser.embedded.view import EmbeddedView
from devoud.browser.web.view import BrowserWebView
from devoud.browser.web.search_engines import search_engines
from devoud.browser.pages.observer import PagesObserver


class AbstractPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('browser_page')
        self.tab_widget = parent
        self.window = parent.window()
        self.FS = self.window.FS
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.layout().addWidget(self.progress_bar)

        self.view_spliter = QSplitter(Qt.Vertical)
        self.layout().addWidget(self.view_spliter)

        self.url = None
        self.view = None
        self.title = None

    def create_web_view(self):
        if self.view is not None:
            self.view.deleteLater()
        self.view = BrowserWebView(self)
        self.view.titleChanged.connect(lambda new_title: self.update_title(new_title))
        self.view.page().urlChanged.connect(self.url_changed)
        self.view.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.view.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.view.setAttribute(Qt.WA_DeleteOnClose)
        self.view.page().fullScreenRequested.connect(self.FullscreenRequest)
        self.view.loadStarted.connect(self.loadStartedHandler)
        self.view.loadProgress.connect(self.loadProgressHandler)
        self.view.loadFinished.connect(self.loadFinishedHandler)
        self.view_spliter.addWidget(self.view)

    def create_embedded_view(self, url='devoud://void'):
        print(f'[Страница]: Открытие встроенной страницы ({url})')
        if self.view is not None:
            self.view.deleteLater()
        self.view = embedded_pages.get(url.partition('#')[0], NotFoundPage)(self)
        self.view.setAttribute(Qt.WA_DeleteOnClose)
        self.view_spliter.addWidget(self.view)

    def load(self, url: str, allow_search=False):
        url = redirects.get(url, url)  # если редирект не найден, то значение остается
        self.url = url

        if is_url(url):
            # если это ссылка, то блокируем поиск
            allow_search = False

        formatted_url = QUrl.fromUserInput(url).toString()

        if (self.view is None or self.view.embedded) and ulr_type(url) is BrowserWebView:
            self.create_web_view()
        elif (self.view is None or not self.view.embedded) and ulr_type(url) is EmbeddedView:
            self.create_embedded_view(url)
        elif self.view.embedded and ulr_type(url) is EmbeddedView:
            self.create_embedded_view(url)

        if not self.view.embedded:
            if allow_search:
                # при разрешении вставляем текст в поисковый движок
                self.view.load(f'{search_engines[self.window.address_panel.search_box.currentText()][0]}{url}')
            else:
                self.view.load(formatted_url)

        PagesObserver.control_update_lists()
        self.update_title(self.view.title)

    def stop(self):
        self.view.stop()

    def reload(self):
        self.view.reload()

    def back(self):
        self.view.back()

    def forward(self):
        self.view.forward()

    def url_changed(self, url):
        if isinstance(url, QUrl):
            self.url = url.toString()
        if self.FS.get_option('saveHistory'):
            with open(f'{self.FS.config_dir()}/history', 'a') as history_file:
                history_file.write(self.url + '\n')
        if self.tab_widget.currentWidget() == self:
            self.window.address_line_edit.setText(self.url)
            self.window.address_line_edit.setCursorPosition(0)
            self.window.check_state_bookmark()
        PagesObserver.control_update_lists()

    def update_title(self, title):
        self.title = title
        index = self.tab_widget.indexOf(self)
        self.tab_widget.setTabText(index, title)
        if self.tab_widget.currentWidget() == self:
            self.window.set_title(title)

    @QtCore.Slot("QWebEngineFullScreenRequest")
    def FullscreenRequest(self, request):
        request.accept()
        if request.toggleOn():
            self.view.setParent(None)
            self.view.showFullScreen()
        else:
            self.layout().addWidget(self.view)
            self.view.showNormal()

    @QtCore.Slot()
    def loadStartedHandler(self):
        self.window.address_panel.update_button.hide()
        self.window.address_panel.stop_load_button.show()
        print(f"[Страница]: Начата загрузка страницы ({self.url})")

    @QtCore.Slot(int)
    def loadProgressHandler(self, progress):
        self.progress_bar.setValue(progress)
        print(f"[Страница]: {progress}% ({self.url})")

    @QtCore.Slot()
    def loadFinishedHandler(self):
        self.window.address_panel.update_button.show()
        self.window.address_panel.stop_load_button.hide()
        self.progress_bar.setValue(0)
        print(f"[Страница]: Страница загружена ({self.url})")
