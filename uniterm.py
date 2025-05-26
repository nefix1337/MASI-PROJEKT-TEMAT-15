import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen, QFontMetrics
from PyQt5.QtGui import QBrush, QColor

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
        
        # x1
        x1_row = QHBoxLayout()
        x1_row.addWidget(QLabel("x1"))
        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText("Wpisz wartość")
        self.x1_input.textChanged.connect(self.update_variables)
        x1_row.addWidget(self.x1_input)
        op1_layout.addLayout(x1_row)
        
        # y1
        y1_row = QHBoxLayout()
        y1_row.addWidget(QLabel("y1"))
        self.y1_input = QLineEdit()
        self.y1_input.setPlaceholderText("Wpisz wartość")
        self.y1_input.textChanged.connect(self.update_variables)
        y1_row.addWidget(self.y1_input)
        op1_layout.addLayout(y1_row)
        
        # z1
        z1_row = QHBoxLayout()
        z1_row.addWidget(QLabel("z1"))
        self.z1_input = QLineEdit()
        self.z1_input.setPlaceholderText("Wpisz wartość")
        self.z1_input.textChanged.connect(self.update_variables)
        z1_row.addWidget(self.z1_input)
        op1_layout.addLayout(z1_row)
        
        # Przycisk eliminacji 1
        # self.btn_elim1 = QPushButton("Dodaj eliminację 1")
        # self.btn_elim1.clicked.connect(self.perform_elimination_1)
        # op1_layout.addWidget(self.btn_elim1)
        
        right_layout.addLayout(op1_layout)
        right_layout.addSpacing(30)
        
        # Druga operacja
        op2_layout = QVBoxLayout()
        
        # x2
        x2_row = QHBoxLayout()
        x2_row.addWidget(QLabel("x2"))
        self.x2_input = QLineEdit()
        self.x2_input.setPlaceholderText("Wpisz wartość")
        self.x2_input.textChanged.connect(self.update_variables)
        x2_row.addWidget(self.x2_input)
        op2_layout.addLayout(x2_row)
        
        # y2
        y2_row = QHBoxLayout()
        y2_row.addWidget(QLabel("y2"))
        self.y2_input = QLineEdit()
        self.y2_input.setPlaceholderText("Wpisz wartość")
        self.y2_input.textChanged.connect(self.update_variables)
        y2_row.addWidget(self.y2_input)
        op2_layout.addLayout(y2_row)
        
        # z2
        z2_row = QHBoxLayout()
        z2_row.addWidget(QLabel("z2"))
        self.z2_input = QLineEdit()
        self.z2_input.setPlaceholderText("Wpisz wartość")
        self.z2_input.textChanged.connect(self.update_variables)
        z2_row.addWidget(self.z2_input)
        op2_layout.addLayout(z2_row)
        
        # Przycisk eliminacji 2
        # self.btn_elim2 = QPushButton("Dodaj eliminację 2")
        # self.btn_elim2.clicked.connect(self.perform_elimination_2)
        # op2_layout.addWidget(self.btn_elim2)
        
        right_layout.addLayout(op2_layout)
        right_layout.addStretch(1)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        
        self.setLayout(main_layout)
        
    def update_variables(self):
        x1_val = self.x1_input.text()
        y1_val = self.y1_input.text()
        z1_val = self.z1_input.text()
        x2_val = self.x2_input.text()
        y2_val = self.y2_input.text()
        z2_val = self.z2_input.text()
        
        # Aktualizuj także zmienne w głównej klasie
        self.x1 = x1_val
        self.y1 = y1_val
        self.z1 = z1_val
        self.x2 = x2_val
        self.y2 = y2_val
        self.z2 = z2_val
        
        self.drawing_widget.update_variables(x1_val, y1_val, z1_val, 
                                           x2_val, y2_val, z2_val)
    
   

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
        
        # Sprawdź czy wszystkie pola pierwszej operacji są wypełnione
        self.show_elimination_1 = bool(x1 and y1 and z1)
        
        # Sprawdź czy wszystkie pola drugiej operacji są wypełnione
        self.show_elimination_2 = bool(x2 and y2 and z2)
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Ustawienia czcionki
        font = QFont("Arial", 12)
        painter.setFont(font)
        
        # Pozycje
        start_x = 50
        start_y = 80
        spacing = 150
        
        # Rysowanie etykiet
        painter.setPen(QPen(Qt.black, 1))
        painter.drawText(20, 50, "Uniterm 1")
        painter.drawText(20, 50 + spacing, "Uniterm 2")
        painter.drawText(20, 50 + 2 * spacing, "Zamiana")
        
        # Rysowanie pierwszej operacji jeśli pola są wypełnione
        if self.show_elimination_1:
            self.draw_operation(painter, start_x, start_y, self.x1, self.y1, self.z1)
        
        # Rysowanie drugiej operacji jeśli pola są wypełnione
        if self.show_elimination_2:
            self.draw_operation(painter, start_x, start_y + spacing, self.x2, self.y2, self.z2)
    
    def draw_operation(self, painter, x, y, term1, term2, term3):
        # Tworzenie tekstu termów
        term_text = f"{term1} , {term2} , {term3}"
        
        # Obliczanie szerokości tekstu
        font_metrics = QFontMetrics(painter.font())
        text_width = font_metrics.horizontalAdvance(term_text)
        
        # Dodanie marginesu po bokach (po 10 pikseli z każdej strony)
        margin = 10
        line_length = text_width + 2 * margin
        
        # Rysowanie linii poziomej (czarna) - dopasowana do długości tekstu
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x, y, x + line_length, y)
        
        # Rysowanie pionowych kresek na końcach
        painter.drawLine(x, y - 12, x, y + 12)
        painter.drawLine(x + line_length, y - 12, x + line_length, y + 12)
        
        # Pozycjonowanie termów (czarny tekst) - wyśrodkowane pod kreską
        painter.setPen(QPen(Qt.black, 1))
        term_y = y + 25
        
        # Rysowanie termów pod kreską - wyśrodkowane
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