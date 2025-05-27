import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFrame, 
                            QDialog, QRadioButton, QButtonGroup)
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
        
        # Zmienne dla wyniku zamiany
        self.replacement_result = None
        self.replacement_done = False
        self.replacement_position = None  # "x1" lub "y1"
        
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
        right_layout.addSpacing(30)
        
        # Przycisk Zamiana
        self.btn_zamiana = QPushButton("Zamiana")
        self.btn_zamiana.clicked.connect(self.open_replacement_dialog)
        right_layout.addWidget(self.btn_zamiana)
        
        right_layout.addStretch(1)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        self.setLayout(main_layout)

        self.apply_styles()

    def update_variables(self):
        self.x1 = self.x1_input.text()
        self.y1 = self.y1_input.text()
        self.z1 = self.z1_input.text()
        self.x2 = self.x2_input.text()
        self.y2 = self.y2_input.text()
        self.z2 = self.z2_input.text()

        self.drawing_widget.update_variables(
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
            self.replacement_result,
            self.replacement_done,
            self.replacement_position
        )
    
    def open_replacement_dialog(self):
        dialog = ReplacementDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            selected_variable = dialog.get_selected_variable()
            self.perform_replacement(selected_variable)

    def perform_replacement(self, selected_variable):
        """Wykonuje operację zamiany i oblicza wynik"""
        # Wstawiona wartość jako osobny uniterm
        inserted_uniterm = {
            'x': self.x2,
            'y': self.y2, 
            'z': self.z2
        }
        
        if selected_variable == "x1":
            # Zamiana x1 - podstawiamy cały uniterm 2 pod x1
            result_x = inserted_uniterm
            result_y = self.y1
            result_z = self.z1
        elif selected_variable == "y1":
            # Zamiana y1 - podstawiamy cały uniterm 2 pod y1
            result_x = self.x1
            result_y = inserted_uniterm
            result_z = self.z1
        else:
            return
        
        self.replacement_result = (result_x, result_y, result_z)
        self.replacement_done = True
        self.replacement_position = selected_variable
        
        print(f"Zamiana wykonana: {selected_variable} -> uniterm 2")
        print(f"Status zamiany: {self.replacement_done}")
        print(f"Pozycja zamiany: {self.replacement_position}")
        
        # Aktualizuj rysunek
        self.drawing_widget.update_variables(
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
            self.replacement_result,
            self.replacement_done,
            self.replacement_position
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
        self.replacement_result = None
        self.replacement_done = False
        self.replacement_position = None
        self.show_elimination_1 = False
        self.show_elimination_2 = False
        self.show_replacement = False
        self.setMinimumHeight(400)

    def update_variables(self, x1, y1, z1, x2, y2, z2, replacement_result=None, replacement_done=False, replacement_position=None):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.replacement_result = replacement_result
        self.replacement_done = replacement_done
        self.replacement_position = replacement_position
        self.show_elimination_1 = bool(x1 and y1 and z1)
        self.show_elimination_2 = bool(x2 and y2 and z2)
        self.show_replacement = bool(replacement_result)
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
        
        # Tytuł "Zamiana" z niebieskim napisem po prawej
        painter.drawText(20, 50 + 2 * spacing, "Zamiana")
        if self.replacement_done:
            painter.setPen(QPen(Qt.blue, 1))
            info_text = f"{self.replacement_position} -> uniterm 2"
            painter.drawText(120, 50 + 2 * spacing, info_text)

        painter.setPen(QPen(Qt.black, 1))

        if self.show_elimination_1:
            self.draw_operation(painter, start_x, start_y, self.x1, self.y1, self.z1)

        if self.show_elimination_2:
            self.draw_operation(painter, start_x, start_y + spacing, self.x2, self.y2, self.z2)
            
        if self.show_replacement:
            result_x, result_y, result_z = self.replacement_result
            self.draw_replacement_operation(painter, start_x, start_y + 2 * spacing, result_x, result_y, result_z)

    def draw_operation(self, painter, x, y, term1, term2, term3):
        term_text = f"{term1} ; {term2} ; {term3}"
        font_metrics = QFontMetrics(painter.font())
        text_width = font_metrics.horizontalAdvance(term_text)
        margin = 12
        line_length = max(text_width + 2 * margin, 150)  # Minimum szerokość dla długich tekstów

        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x, y, x + line_length, y)
        painter.drawLine(x, y - 12, x, y + 12)
        painter.drawLine(x + line_length, y - 12, x + line_length, y + 12)

        painter.setPen(QPen(Qt.black, 1))
        term_y = y + 25
        text_x = x + margin
        
        # Sprawdź czy tekst mieści się w linii, jeśli nie - zmniejsz czcionkę
        if text_width > line_length - 2 * margin:
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
        
        painter.drawText(text_x, term_y, term_text)

    def draw_replacement_operation(self, painter, x, y, term1, term2, term3):
        """Rysuje operację zamiany z wstawioną wartością jako osobny poziomy uniterm na tym samym poziomie"""
        font_metrics = QFontMetrics(painter.font())
        
        # Najpierw znajdź pozycje dla zwykłych termów i wstawionego unitermu
        terms = [term1, term2, term3]
        term_positions = []
        current_x = x + 12
        
        # Oblicz pozycje wszystkich termów
        for i, term in enumerate(terms):
            if isinstance(term, dict):
                # To jest wstawiony uniterm - zarezerwuj miejsce
                inserted_text = f"{term['x']} ; {term['y']} ; {term['z']}"
                width = font_metrics.horizontalAdvance(inserted_text) + 24  # margines dla linii unitermu
                term_positions.append({'type': 'inserted', 'x': current_x, 'width': width, 'text': inserted_text})
                current_x += width
            else:
                # Zwykły term
                text = str(term)
                width = font_metrics.horizontalAdvance(text)
                term_positions.append({'type': 'normal', 'x': current_x, 'width': width, 'text': text})
                current_x += width
            
            # Dodaj separator (oprócz ostatniego elementu)
            if i < len(terms) - 1:
                separator = " ; "
                current_x += font_metrics.horizontalAdvance(separator)
        
        # Oblicz całkowitą szerokość głównej linii
        total_width = current_x - x
        line_length = max(total_width, 200)
        
        # Rysowanie głównej linii unitermu
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x, y, x + line_length, y)
        painter.drawLine(x, y - 12, x, y + 12)
        painter.drawLine(x + line_length, y - 12, x + line_length, y + 12)
        
        # Rysowanie poszczególnych termów
        current_x = x + 12
        text_y = y + 25
        
        for i, (term, pos_info) in enumerate(zip(terms, term_positions)):
            if pos_info['type'] == 'inserted':
                # Rysuj wstawiony uniterm jako osobną linię na tym samym poziomie co tekst
                uniterm_y = text_y - 15  # Na tym samym poziomie co główny tekst
                uniterm_width = pos_info['width']
                
                # Linia dla wstawionego unitermu
                painter.setPen(QPen(Qt.black, 2))
                painter.drawLine(current_x, uniterm_y, current_x + uniterm_width, uniterm_y)
                painter.drawLine(current_x, uniterm_y - 6, current_x, uniterm_y + 6)
                painter.drawLine(current_x + uniterm_width, uniterm_y - 6, current_x + uniterm_width, uniterm_y + 6)
                
                # Tekst wstawionego unitermu
                painter.setPen(QPen(Qt.black, 1))
                painter.drawText(current_x + 12, uniterm_y + 15, pos_info['text'])
                
                current_x += uniterm_width
            else:
                # Zwykły term na głównej linii
                painter.setPen(QPen(Qt.black, 1))
                painter.drawText(current_x, text_y, pos_info['text'])
                current_x += pos_info['width']
            
            # Separator
            if i < len(terms) - 1:
                painter.setPen(QPen(Qt.black, 1))
                separator = " ; "
                painter.drawText(current_x, text_y, separator)
                current_x += font_metrics.horizontalAdvance(separator)


class ReplacementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zamiana")
        self.setModal(True)
        self.setFixedSize(300, 180)
        
        layout = QVBoxLayout()
        
        # Opis
        description = QLabel("Wybierz wartość która ma być zamieniona:")
        layout.addWidget(description)
        
        # Grupa przycisków radiowych
        self.button_group = QButtonGroup()
        
        self.x1_radio = QRadioButton("x1 (podstaw cały uniterm 2)")
        self.y1_radio = QRadioButton("y1 (podstaw cały uniterm 2)")
        
        # Domyślnie zaznacz pierwszy
        self.x1_radio.setChecked(True)
        
        self.button_group.addButton(self.x1_radio)
        self.button_group.addButton(self.y1_radio)
        
        layout.addWidget(self.x1_radio)
        layout.addWidget(self.y1_radio)
        
        # Przyciski OK i Anuluj
        buttons_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Anuluj")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def get_selected_variable(self):
        if self.x1_radio.isChecked():
            return "x1"
        elif self.y1_radio.isChecked():
            return "y1"
        return None


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