import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.Browse.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'XML files (*.xml)')
        self.filename.setText(fname[0])
        path = fname[0]
        with open(path, "r") as f:
            data = f.read()
            self.textEdit.setText(data)
            print(data)

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1000)
widget.setFixedHeight(900)
widget.show()
sys.exit(app.exec_())

if __name__ == "__main__":
    main()
