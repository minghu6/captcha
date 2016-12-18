# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtWidgets import QGridLayout

from minghu6.graphic.captcha.get_image import get_image
from minghu6.graphic.captcha.recognise import tesseract
from minghu6.graphic.captcha.url_captcha import url_captcha_dict

from minghu6.internet.simulate_logon import url_logon_dict


class Ui_MainWindow():

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 442)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #self.digit_captcha_label = QtWidgets.QLabel()
        #self.digit_captcha_label.setObjectName("digit_captcha_label")

        #self.digit_captcha_lcd = QtWidgets.QLCDNumber()
        #self.digit_captcha_lcd.setObjectName("digit_captcha_lcd")

        #self.digit_captcha_lcd.setFont(font)
        self.simulate_logon_btn = QtWidgets.QPushButton('simulate logon')


        self.raw_captcha_view = QtWidgets.QGraphicsView()
        self.raw_captcha_view.setObjectName("raw_captcha_view")

        self.url_input_line = QtWidgets.QLineEdit()
        self.url_input_line.setObjectName("url_line")

        self.url_input_label = QtWidgets.QLabel()
        self.url_input_label.setObjectName("url_label")

        self.captcha_label = QtWidgets.QLabel()


        self.captcha_text = QtWidgets.QTextBrowser()


        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setPixelSize(18)
        self.captcha_text.setFont(font)
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

        self.grid.addWidget(self.captcha_label, 3, 1)
        self.grid.addWidget(self.captcha_text, 3, 2)
        self.grid.addWidget(self.simulate_logon_btn, 5, 1, 3, 3)


        self.centralwidget.setLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.setSlot()


    def setSlot(self):
        def url_input_line_func():
            url = self.url_input_line.text()
            self.url = url
            qurl = QUrl(url)


            #url_captcha = url_captcha_dict.get(url, url)
            # load url into browser frame
            if not hasattr(self, 'session_dict'):
               self.session_dict = {}
            #self.session_dict = {}
            session1 = self.session_dict.get(url, None)
            responseSet = url_captcha_dict[url](session=session1)

            url_captcha, url_session = responseSet[:2]
            self.params_dict = responseSet[-1]
            html = responseSet[2]


            _, imgPath = get_image(url_captcha, session=url_session)
            result = ''
            try:

                result = tesseract(imgPath, limit_config='letters_digits')
                #result = tesseract(url_captcha)
            except Exception as ex:
                print(ex)

            finally:
                self.result = result

            # update url:session
            self.session_dict[url] = url_session
            cookies1 = url_session.cookies.get_dict()
            #cookies1 = responseSet[2]



            scene = QtWidgets.QGraphicsScene()
            image=QtGui.QPixmap(imgPath)
            scene.addPixmap(image)
            self.raw_captcha_view.setScene(scene)

            self.captcha_text.clear() #
            self.captcha_text.setText(result)

            cookieStore = self.browser.page().profile().cookieStore()
            #cookieStore.deleteAllCookies()

            cookies2=QNetworkCookie()
            for name, value in cookies1.items():
                #print(name, value)
                cookies2.setName(name.encode())
                cookies2.setValue(value.encode())
                cookies2.setDomain(url)
                cookies2.setPath(url)

                cookieStore.setCookie(cookies2, qurl)


            #print(cookieStore.loadAllCookies())


            #self.browser.load(qurl)
            self.browser.setHtml(html, qurl)

        def simulate_logon_func():

            from minghu6.graphic.captcha.url_captcha import CAPTCHA_ID
            self.params_dict[CAPTCHA_ID] = self.result

            html = url_logon_dict[self.url](self.session_dict[self.url],
                                            **self.params_dict)

            self.browser.setHtml(html, QUrl(self.url))


        self.url_input_line.returnPressed.connect(url_input_line_func)
        self.simulate_logon_btn.clicked.connect(simulate_logon_func)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.digit_captcha_label.setText(_translate("MainWindow", "digit captcha"))
        self.url_input_label.setText(_translate("MainWindow", "Url"))
        self.captcha_label.setText(_translate("MainWindow", "catcha"))
        self.menuMenu.setTitle(_translate("MainWindow", "Author"))
        self.actionAuthor.setText(_translate("MainWindow", "庄&&刘&&冯"))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())