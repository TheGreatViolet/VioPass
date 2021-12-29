import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import passgen
import webbrowser


class About(QWidget):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.title='About VioPass'
        self.setStyleSheet(open('stylesheet.css').read())
        self.width=400
        self.height=280
        self.aboutUI()
    
    def aboutUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.label = QLabel("About VioPass:", self)
        self.ver = QLabel("Version 2.0.0, Style and Security Update", self)
        self.developer = QLabel("Developed by Violet Hayes", self)
        self.license = QLabel("GNU GPL 3.0 License", self)

        self.label.move(20, 20)
        self.ver.move(20, 60)
        self.developer.move(20, 80)
        self.license.move(20, 100)

        self.repobutton = QPushButton("View GitHub Repo", self)
        self.repobutton.resize(140, 20)
        self.repobutton.move(220, 240)

        self.repobutton.clicked.connect(self.openrepo)

    def openrepo(self):
        webbrowser.open('https://github.com/TheGreatViolet/VioPass/tree/main')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title='VioPass 2.0.0'
        self.setStyleSheet(open('stylesheet.css').read())
        self.width=660
        self.height=480
        self.masterPassPrompt()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.nameentry = QLineEdit(self)
        self.nameentry.move(360,20)
        self.nameentry.resize(280,40)
        self.generatebutton = QPushButton('Generate Password', self)
        self.generatebutton.move(360,80)
        self.generatebutton.resize(140, 40)

        self.generatebutton.clicked.connect(self.ongen)

        self.passlist = QListWidget(self)
        self.passlist.move(0,0)
        self.passlist.resize(240,480)

        self.passlist.itemClicked.connect(self.displayPassword)

        self.listPasswords()

        self.aboutbutton = QPushButton('About', self)
        self.aboutbutton.resize(60, 20)
        self.aboutbutton.move(580, 440)

        self.aboutbutton.clicked.connect(self.openabout)

        self.show()

    def ongen(self):
        passname = self.nameentry.text()
        if passgen.generatePassword(20, passname) == 1:
            QMessageBox.warning(self, 'Openpass - Error', 'Password already exists, please choose a different name.')
        else:
            self.passlist.addItem(passname)
            QMessageBox.information(self, 'Openpass - Success', 'Password saved to passfile')

    def listPasswords(self):
        passlist = passgen.loadPasswords()
        
        for key in passlist.keys():
            self.passlist.addItem(key)

    def displayPassword(self, item):
        passlist = passgen.loadPasswords()
        QMessageBox.information(self, "Password", 'The password for ' + item.text() + ' is: ' + passlist[item.text()])

    def masterPassPrompt(self):
        passlist = passgen.loadPasswords()
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        if "masterpass" in passlist.keys():
            self.prompt = QLabel("Please enter your master password", self)
            self.prompt.move(20,20)
            self.prompt.resize(600,40)
            self.promptbox = QLineEdit(self)
            self.promptbox.move(20,60)
            self.promptbox.resize(280,40)
            self.enterbutton = QPushButton("Enter", self)
            self.enterbutton.move(20,120)

            self.enterbutton.clicked.connect(self.checkMasterPass)
            
            self.show()

        else:
            self.prompt = QLabel("Please enter a master password that will be used to unlock VioPass", self)
            self.prompt.move(20,20)
            self.prompt.resize(600,40)
            self.promptbox = QLineEdit(self)
            self.promptbox.move(20,60)
            self.promptbox.resize(600,40)
            self.confirmlabel = QLabel("Please confirm your master password", self)
            self.confirmlabel.move(20,100)
            self.confirmlabel.resize(600,40)
            self.confirm = QLineEdit(self)
            self.confirm.move(20,140)
            self.confirm.resize(600,40)
            self.enterbutton = QPushButton("Enter", self)
            self.enterbutton.move(20, 200)

            self.enterbutton.clicked.connect(self.checkAndSave)

            self.show()
    
    def checkMasterPass(self):
        entered = self.promptbox.text()
        passlist = passgen.loadPasswords()

        if passlist["masterpass"] == entered:
            self.prompt.hide()
            self.promptbox.hide()
            self.enterbutton.hide()

            self.close()
            self.initUI()
        else:
            QMessageBox.warning(self, "Incorrect", "The entered password is incorrect, try again")

    def checkAndSave(self):
        if self.promptbox.text() == self.confirm.text():
            passlist = passgen.loadPasswords()
            passlist["masterpass"] = self.promptbox.text()
            passgen.writePasswords(passlist)

            self.prompt.hide()
            self.promptbox.hide()
            self.confirmlabel.hide()
            self.confirm.hide()
            self.enterbutton.hide()

            self.close()
            self.initUI()
        else:
            QMessageBox.warning(self, "Error", "The entered passwords don't match.")

    def openabout(self):
        self.aboutwindow = About()
        self.aboutwindow.show()

    def closeEvent(self, event):
        widgetlist = QApplication.topLevelWidgets()
        numwindows = len(widgetlist)
        if numwindows > 1:
            self.aboutwindow = About()
            self.aboutwindow.close()


def main():
    passgen.checkFiles()
    app=QApplication(sys.argv)
    ex=App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()