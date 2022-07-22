import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

print("If you're on Fedora 35 or higher, please execute this command before starting the browser!")
print('export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"')
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.startpage.com/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # navbar
        # space taker
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('[<]', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('[>]', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('[Ø]', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('[^]', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)
        

		# new tab button
		new_tab_btn = QAction("[+]", self)
		new_tab_btn.triggered.connect(self.newTabProcess)
		self.navbar.addAction(new_tab_btn)

		# close tab button
		close_tab_btn = QAction("[×]", self)
		close_tab_btn.triggered.connect(self.closeTabProcess)
		self.navbar.addAction(close_tab_btn)
        
    def navigate_home(self):
        self.browser.setUrl(QUrl('https://lintine.github.io/newtab/'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        
    def tabSwitcherProcess(self):
		self.browser_index = self.tab_switcher.currentIndex()
		# show the correct browser
		self.takeCentralWidget()
		self.setCentralWidget(self.browsers[self.browser_index])
		# set the window title to "Blazenet • " + page title + " • " + url
		self.setWindowTitle("Minisurfer Window • " + self.browser().page().title() + " • " + self.browser().url().toString())
	
	def newTabProcess(self):
		self.browsers.append(QWebEngineView())
		self.tab_switcher.addItem("New Tab")
		self.tab_switcher.setCurrentIndex(len(self.browsers) - 1)
		self.tabSwitcherProcess()
		# when the page changes, call onPageChangedProcess()
		self.browser().urlChanged.connect(self.onPageChangedProcess)
		# when the browser loads a page, call onPageLoadProcess()
		self.browser().loadFinished.connect(self.onPageLoadProcess)
		# homepage
		try: self.homeProcess()
		except: pass
	
	def closeTabProcess(self):
		if len(self.browsers) > 1:
			self.browsers.pop(self.browser_index)
			self.tab_switcher.removeItem(self.browser_index)
			if self.browser_index >= len(self.browsers):
				self.browser_index = len(self.browsers) - 1
			self.tabSwitcherProcess()
	

app = QApplication(sys.argv)
QApplication.setApplicationName('Minisurfer')
window = MainWindow()
app.exec_()
