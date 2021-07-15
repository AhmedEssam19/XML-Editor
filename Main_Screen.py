import sys
import xmltodict
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMenuBar, QMainWindow, QAction, QMessageBox

from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from PyQt5.QtWidgets import QWidget, QLineEdit, QPlainTextEdit, QVBoxLayout
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QRegExpValidator, QSyntaxHighlighter, QTextCharFormat

from CodeFormat import *
from compress import *
from XMLTree import *

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super(SyntaxHighlighter, self).__init__(parent)
        self._highlight_lines = dict()

    def highlight_line(self, line, fmt):
        if isinstance(line, int) and line >= 0 and isinstance(fmt, QTextCharFormat):
            self._highlight_lines[line] = fmt
            tb = self.document().findBlockByLineNumber(line)
            self.rehighlightBlock(tb)

    def clear_highlight(self):
        self._highlight_lines = dict()
        self.rehighlight()

    def highlightBlock(self, text):
        line = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(line)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)


class MainWindow(QMainWindow, QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        #self.Browse.clicked.connect(self.XML2JSON)
        self.create_menu()
        self.data = ""
        self.lines = [5,8,9]
        self._highlighter = SyntaxHighlighter(self.textEdit.document())

        self.show()


    def onTextChanged(self):
        self.lines = mark_error(str(self.textEdit.toPlainText()))
        data = edit_string(str(self.textEdit.toPlainText()))
        self.textEdit.setText(data)
        print(self.lines)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("yellow"))
        self._highlighter.clear_highlight()
        for i in range(0,len(self.lines)):
            self._highlighter.highlight_line(self.lines[i]-1, fmt)



    def browsefiles(self):
        # actionNew_File.triggered.connect(self.browsefiles)
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'XML files (*.xml)')
        self.filename.setText(fname[0])
        path = fname[0]
        with open(path, "r") as f:
            data = f.read()
            self.textEdit.setText(data)
            self.data = data
            print(data)

    def fixError(self):
        data = fix_error(str(self.textEdit.toPlainText()))
        print(data)
        self.textEdit.setText(data)

    def transfer_to_json(self):
        tree = XMLTree(str(self.textEdit.toPlainText()))
        print(tree.get_root().tag)
        data = XML2json(tree)
        print("hiii2")

        self.textEdit.setText(str(data))
        print(data)

    def format(self):
        data = prettify_code(str(self.textEdit.toPlainText()))
        print(data)
        self.textEdit.setText(data)

    def compress_space(self):
        data = minify(str(self.textEdit.toPlainText()))
        print(data)
        self.textEdit.setText(data)


    def compress_huffman(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'XML files (*.xml)')
        self.filename.setText(fname[0])
        path = fname[0]
        compress(path)
        QMessageBox.about(self, "Success", "File Compressed Successfully in the same directory")

    def expand_huffman(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'Compressed Files (*.m3a)')
        self.filename.setText(fname[0])
        path = fname[0]
        data = expand(path)
        print(data)
        QMessageBox.about(self, "Success", "File Expanded you can save it now in xml extension")
        self.textEdit.setText(data)


    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("Edit")
        searchMenu = mainMenu.addMenu("Font")
        helpMenu = mainMenu.addMenu("Help")

        openAction = QAction(QIcon('open.png'), "Open", self)
        openAction.setShortcut("Ctrl+O")

        saveAction = QAction(QIcon('save.png'), "Save", self)
        saveAction.setShortcut("Ctrl+S")

        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+X")

        view_errorAction = QAction(QIcon('exit.png'), "View Error", self)
        view_errorAction.setShortcut("Ctrl+E")

        solve_errorAction = QAction(QIcon('slove.png'), "Solve Error", self)
        solve_errorAction.setShortcut("Ctrl+V")

        format_Action = QAction(QIcon('format.png'), "Format File", self)
        format_Action.setShortcut("Ctrl+F")

        compress_space_Action = QAction(QIcon('compress_space.png'), "Compress File by spacing", self)
        compress_space_Action.setShortcut("Ctrl+A")

        compress_huffman_Action = QAction(QIcon('compress_huffman.png'), "Compress File by huffman", self)
        compress_huffman_Action.setShortcut("Ctrl+B")

        expand_huffman_Action = QAction(QIcon('compress_huffman.png'), "Expand File", self)
        expand_huffman_Action.setShortcut("Ctrl+P")

        XML2JSON_Action = QAction(QIcon('xml.png'), "Transfer to JSON", self)
        XML2JSON_Action.setShortcut("Ctrl+J")

        saveAction.triggered.connect(self.save_file)
        exitAction.triggered.connect(self.exit_app)
        openAction.triggered.connect(self.browsefiles)

        view_errorAction.triggered.connect(self.onTextChanged)
        solve_errorAction.triggered.connect(self.fixError)
        format_Action.triggered.connect(self.format)

        compress_space_Action.triggered.connect(self.compress_space)
        compress_huffman_Action.triggered.connect(self.compress_huffman)
        expand_huffman_Action.triggered.connect(self.expand_huffman)
        XML2JSON_Action.triggered.connect(self.transfer_to_json)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        viewMenu.addAction(view_errorAction)
        viewMenu.addAction(solve_errorAction)
        viewMenu.addAction(format_Action)

        editMenu.addAction(compress_space_Action)
        editMenu.addAction(compress_huffman_Action)
        editMenu.addAction(expand_huffman_Action)
        editMenu.addAction(XML2JSON_Action)

    def save_file(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', options=QFileDialog.DontUseNativeDialog)
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    def exit_app(self):
        self.close()


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1500)
widget.setFixedHeight(900)
widget.show()
sys.exit(app.exec_())

if __name__ == "__main__":
    main()
