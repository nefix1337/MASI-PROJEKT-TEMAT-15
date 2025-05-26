import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen, QFontMetrics


class UnitermWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.x1 = "A"
        self.y1 = "A"
        self.z1 = "u"
        self.x2 = "p"
        self.y2 = "q"
        self.z2 = "r"
        
        self.initUI()
    
    def initUI(self):
        main_layout = QHBoxLayout()
        
        # Lewa strona - rysowanie unitermów
        self.drawing_widget = UnitermDrawing()
        self.drawing_widget.setMinimumWidth(400)
        main_layout.addWidget(self.drawing_widget)
        
        # Pionowa linia separująca
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setLineWidth(2)
        main_layout.addWidget(separator)
        
        # Prawa strona - interfejs wprowadzania
        right_panel = QWidget()
        right_panel.setFixedWidth(300)
        right_layout = QVBoxLayout()
        
        # Pierwsza operacja
        op1_layout = QVBoxLayout()
        x1_row = QHBoxLayout()
        x1_row.addWidget(QLabel("x1:"))
        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText("Wpisz wartość")
        self.x1_input.textChanged.connect(self.update_variables)
        x1_row.addWidget(self.x1_input)
        op1_layout.addLayout(x1_row)

        y1_row = QHBoxLayout()
        y1_row.addWidget(QLabel("y1:"))
        self.y1_input = QLineEdit()
        self.y1_input.setPlaceholderText("Wpisz wartość")
        self.y1_input.textChanged.connect(self.update_variables)
        y1_row.addWidget(self.y1_input)
        op1_layout.addLayout(y1_row)

        z1_row = QHBoxLayout()
        z1_row.addWidget(QLabel("z1:"))
        self.z1_input = QLineEdit()
        self.z1_input.setPlaceholderText("Wpisz wartość")
        self.z1_input.textChanged.connect(self.update_variables)
        z1_row.addWidget(self.z1_input)
        op1_layout.addLayout(z1_row)

        right_layout.addLayout(op1_layout)
        right_layout.addSpacing(30)

        # Druga operacja
        op2_layout = QVBoxLayout()
        x2_row = QHBoxLayout()
        x2_row.addWidget(QLabel("x2:"))
        self.x2_input = QLineEdit()
        self.x2_input.setPlaceholderText("Wpisz wartość")
        self.x2_input.textChanged.connect(self.update_variables)
        x2_row.addWidget(self.x2_input)
        op2_layout.addLayout(x2_row)

        y2_row = QHBoxLayout()
        y2_row.addWidget(QLabel("y2:"))
        self.y2_input = QLineEdit()
        self.y2_input.setPlaceholderText("Wpisz wartość")
        self.y2_input.textChanged.connect(self.update_variables)
        y2_row.addWidget(self.y2_input)
        op2_layout.addLayout(y2_row)

        z2_row = QHBoxLayout()
        z2_row.addWidget(QLabel("z2:"))
        self.z2_input = QLineEdit()
        self.z2_input.setPlaceholderText("Wpisz wartość")
        self.z2_input.textChanged.connect(self.update_variables)
        z2_row.addWidget(self.z2_input)
        op2_layout.addLayout(z2_row)

        right_layout.addLayout(op2_layout)
        right_layout.addStretch(1)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        self.setLayout(main_layout)

        self.apply_styles()  # <-- tutaj stylujemy

    def update_variables(self):
        self.x1 = self.x1_input.text()
        self.y1 = self.y1_input.text()
        self.z1 = self.z1_input.text()
        self.x2 = self.x2_input.text()
        self.y2 = self.y2_input.text()
        self.z2 = self.z2_input.text()

        self.drawing_widget.update_variables(
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2
        )

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 14px;
            }

            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 4px;
                background-color: #fdfdfd;
            }

            QLineEdit:focus {
                border: 2px solid #0078d7;
                background-color: #ffffff;
            }

            QLabel {
        
                font-weight: bold;
                
            }

            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #005fa3;
            }

            QFrame {
                background-color: #ddd;
            }
        """)


class UnitermDrawing(QWidget):
    def __init__(self):
        super().__init__()
        self.x1 = ""
        self.y1 = ""
        self.z1 = ""
        self.x2 = ""
        self.y2 = ""
        self.z2 = ""
        self.show_elimination_1 = False
        self.show_elimination_2 = False
        self.setMinimumHeight(400)

    def update_variables(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.show_elimination_1 = bool(x1 and y1 and z1)
        self.show_elimination_2 = bool(x2 and y2 and z2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont("Arial", 12)
        painter.setFont(font)

        start_x = 50
        start_y = 80
        spacing = 150

        painter.setPen(QPen(Qt.black, 1))
        painter.drawText(20, 50, "Uniterm 1")
        painter.drawText(20, 50 + spacing, "Uniterm 2")
        painter.drawText(20, 50 + 2 * spacing, "Zamiana")

        if self.show_elimination_1:
            self.draw_operation(painter, start_x, start_y, self.x1, self.y1, self.z1)

        if self.show_elimination_2:
            self.draw_operation(painter, start_x, start_y + spacing, self.x2, self.y2, self.z2)

    def draw_operation(self, painter, x, y, term1, term2, term3):
        term_text = f"{term1} , {term2} , {term3}"
        font_metrics = QFontMetrics(painter.font())
        text_width = font_metrics.horizontalAdvance(term_text)
        margin = 10
        line_length = text_width + 2 * margin

        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x, y, x + line_length, y)
        painter.drawLine(x, y - 12, x, y + 12)
        painter.drawLine(x + line_length, y - 12, x + line_length, y + 12)

        painter.setPen(QPen(Qt.black, 1))
        term_y = y + 25
        text_x = x + margin
        painter.drawText(text_x, term_y, term_text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program Unitermów - Operacje Eliminowania")
        self.setGeometry(100, 100, 800, 600)
        central_widget = UnitermWidget()
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
