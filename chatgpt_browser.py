# Создаем браузер с помощью Chat GPT и Python за 3 минуты

# Подписывайтесь, чтобы
# быстрее узнавать о
# новых уроках - https://t.me/isartem_bot

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Browser')
        self.show()

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.back_button = QAction('Back')
        self.toolbar.addAction(self.back_button)

        self.forward_button = QAction('Forward')
        self.toolbar.addAction(self.forward_button)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.browse)
        self.toolbar.addWidget(self.urlbar)

        self.web = QWebEngineView()
        self.setCentralWidget(self.web)
        self.back_button.triggered.connect(self.web.back)
        self.forward_button.triggered.connect(self.web.forward)
        self.urlbar.setText('https://www.google.com')
        self.browse()

    def browse(self):
        url = QUrl(self.urlbar.text())
        self.web.load(url)

app = QApplication(sys.argv)
browser = Browser()
sys.exit(app.exec_())

