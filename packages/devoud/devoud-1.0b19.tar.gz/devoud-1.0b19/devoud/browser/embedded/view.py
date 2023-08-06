from devoud.browser import *


class EmbeddedView(QWidget):
    title = "'Embedded Page'"
    url = None

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('embedded_view')
        self.embedded = True

    def load(self, url):
        self.parent().parent().load(url)

    def stop(self):
        pass

    def reload(self):
        self.parent().parent().load(self.url)

    def forward(self):
        pass

    def back(self):
        pass
