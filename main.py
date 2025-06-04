import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFrame, 
                            QDialog, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen, QFontMetrics, QIcon
import psycopg2
from database import *
from gui import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program Unitermów - Operacje Eliminowania")
        self.setGeometry(100, 100, 1000, 800)
        central_widget = UnitermWidget()
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()