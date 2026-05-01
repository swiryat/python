import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QAction, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWebEngineWidgets import QWebEnginePage

class SimpleWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.browser)

        # Создаем панель инструментов
        navtb = self.addToolBar("Navigation")
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to the previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.setStatusTip("Forward to the next page")
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        search_btn = QAction("Search", self)
        search_btn.setStatusTip("Search on the web")
        search_btn.triggered.connect(self.search)
        navtb.addAction(search_btn)

        navtb.addSeparator()

        print_btn = QAction("Print", self)
        print_btn.setStatusTip("Print page")
        print_btn.triggered.connect(self.print_page)
        navtb.addAction(print_btn)

        save_btn = QAction("Save", self)
        save_btn.setStatusTip("Save page")
        save_btn.triggered.connect(self.save_page)
        navtb.addAction(save_btn)

        navtb.addSeparator()

        zoomin_btn = QAction("Zoom In", self)
        zoomin_btn.setStatusTip("Zoom in the page")
        zoomin_btn.triggered.connect(self.zoom_in)
        navtb.addAction(zoomin_btn)

        zoomout_btn = QAction("Zoom Out", self)
        zoomout_btn.setStatusTip("Zoom out the page")
        zoomout_btn.triggered.connect(self.zoom_out)
        navtb.addAction(zoomout_btn)

        navtb.addSeparator()

        mute_btn = QAction("Mute", self)
        mute_btn.setStatusTip("Mute the page")
        mute_btn.triggered.connect(self.mute)
        navtb.addAction(mute_btn)

        navtb.addSeparator()

        about_btn = QAction("About", self)
        about_btn.setStatusTip("About Simple Web Browser")
        about_btn.triggered.connect(self.about)
        navtb.addAction(about_btn)

        navtb.addSeparator()

        developer_btn = QAction("Developer Tools", self)
        developer_btn.setStatusTip("Open Developer Tools")
        developer_btn.triggered.connect(self.toggle_developer_tools)
        navtb.addAction(developer_btn)

        navtb.addSeparator()

        # Добавляем кнопку закрытия окна
        close_btn = QAction("Close", self)
        close_btn.setStatusTip("Close the browser")
        close_btn.triggered.connect(self.close)
        navtb.addAction(close_btn)

        self.browser.urlChanged.connect(self.update_urlbar)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Устанавливаем заглавие окна
        self.setWindowTitle("Simple Web Browser")

        # Устанавливаем размеры окна
        self.setGeometry(100, 100, 1024, 768)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def search(self):
        q = QUrl("https://www.google.com/search?q=" + self.urlbar.text())
        self.browser.setUrl(q)

    def print_page(self):
        self.browser.print(self.print_preview)

    def print_preview(self, printer):
        self.browser.page().printToPdf(printer)

    def save_page(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "HTML Files (*.html);;All Files (*)")
        if file:
            self.browser.page().toHtml(lambda data: self.save(data, file))

    def save(self, data, file):
        with open(file, 'w', encoding='utf-8') as f:
            f.write(data)

    def zoom_in(self):
        self.browser.setZoomFactor(self.browser.zoomFactor() + 0.1)

    def zoom_out(self):
        self.browser.setZoomFactor(self.browser.zoomFactor() - 0.1)

    def mute(self):
        self.browser.page().setAudioMuted(not self.browser.page().isAudioMuted())

    def toggle_developer_tools(self):
        self.browser.page().setDevToolsPage(self.browser.page())
        self.browser.page().triggerAction(QWebEnginePage.InspectElement)

    def about(self):
        about_text = "Simple Web Browser\nVersion 1.0\nPython 3.7, PyQt5\n"
        QMessageBox.about(self, "About Simple Web Browser", about_text)

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

app = QApplication(sys.argv)
QApplication.setApplicationName("Simple Web Browser")
window = SimpleWebBrowser()
app.exec_()
