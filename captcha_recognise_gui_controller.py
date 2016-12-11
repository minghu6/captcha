# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineCore import QWebEngineCookieStore
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import qRed

from minghu6.graphic.captcha.recognise import tesseract
from minghu6.graphic.captcha.url_captcha import url_captcha_dict

class Ui_MainWindow():

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 442)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.digit_captcha_label = QtWidgets.QLabel()
        self.digit_captcha_label.setObjectName("digit_captcha_label")

        self.digit_captcha_lcd = QtWidgets.QLCDNumber()
        self.digit_captcha_lcd.setObjectName("digit_captcha_lcd")
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setPixelSize(18)
        self.digit_captcha_lcd.setFont(font)

        self.raw_captcha_view = QtWidgets.QGraphicsView()
        self.raw_captcha_view.setObjectName("raw_captcha_view")

        self.url_input_line = QtWidgets.QLineEdit()
        self.url_input_line.setObjectName("url_line")

        self.url_input_label = QtWidgets.QLabel()
        self.url_input_label.setObjectName("url_label")

        self.other_captcha_label = QtWidgets.QLabel()
        self.other_captcha_label.setObjectName("other_captcha_label")

        self.other_captcha_text = QtWidgets.QTextBrowser()
        self.other_captcha_text.setObjectName("other_captcha_text")
        self.other_captcha_text.setFont(font)
        #self.other_captcha_text.append('abcde3')



        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")

        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAuthor = QtWidgets.QAction(MainWindow)
        self.actionAuthor.setObjectName("actionAuthor")
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionAuthor)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)






        self.gridLayout = QGridLayout()

        self.browser = QWebEngineView()
        self.browser.setObjectName('browser')


        page = QWebEnginePage()
        self.browser.setPage(page)

        self.grid = self.gridLayout

        self.grid.addWidget(self.url_input_label, 0, 0)
        self.grid.addWidget(self.url_input_line, 1, 0, 1, 5)

        #self.grid.addWidget(self.url_grid, 0, 0)
        self.grid.addWidget(self.browser, 2, 0, 6, 1)
        self.grid.addWidget(self.raw_captcha_view, 2, 1, 1, 3)

        self.grid.addWidget(self.digit_captcha_label, 3, 1)
        self.grid.addWidget(self.digit_captcha_lcd, 3, 2)
        self.grid.addWidget(self.other_captcha_label, 4, 1)
        self.grid.addWidget(self.other_captcha_text, 4, 2)



        self.centralwidget.setLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.setSlot()


    def setSlot(self):
        def url_input_line_func():
            url = self.url_input_line.text()
            qurl = QUrl(url)


            #url_captcha = url_captcha_dict.get(url, url)
            # load url into browser frame
            if not hasattr(self, 'session_dict'):
               self.session_dict = {}

            session1 = self.session_dict.get(url, None)
            responseSet = url_captcha_dict[url](session=session1)
            url_captcha, session2 = responseSet[:2]
            print(session1 is session2, session1)
            self.session_dict[url] = session2
            cookies1 = session2.cookies.get_dict()
            #cookies1 = responseSet[2]
            print(url_captcha)
            print(cookies1)
            try:
                result = tesseract(url_captcha, session=session2)
                #result = tesseract(url_captcha)
            except Exception as ex:
                print(ex)
                result=''

            scene = QtWidgets.QGraphicsScene()
            image=QtGui.QPixmap('captcha')
            scene.addPixmap(image)
            self.raw_captcha_view.setScene(scene)

            from minghu6.algs.var import isnum_str
            if isnum_str(result):
                self.other_captcha_text.clear() #
                self.digit_captcha_lcd.display(result)
            else:

                self.other_captcha_text.clear()
                self.digit_captcha_lcd.display('0') #
                self.other_captcha_text.append(result)

            cookieStore = self.browser.page().profile().cookieStore()
            array_key = QByteArray(' '.join(cookies1.keys()).encode())
            array_value = QByteArray(' '.join(cookies1.values()).encode())
            cookies2=QNetworkCookie(array_key, array_value)
            cookieStore.setCookie(cookies2, qurl)
            self.browser.load(qurl)


        self.url_input_line.returnPressed.connect(url_input_line_func)
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.digit_captcha_label.setText(_translate("MainWindow", "digit captcha"))
        self.url_input_label.setText(_translate("MainWindow", "Url"))
        self.other_captcha_label.setText(_translate("MainWindow", "other catcha"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionAuthor.setText(_translate("MainWindow", "Author"))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())