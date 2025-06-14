from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFrame, 
                            QDialog, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem, QAbstractItemView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen, QFontMetrics, QIcon
from database import *

class UnitermWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.x1 = ""
        self.y1 = ""
        self.z1 = ""
        self.x2 = ""
        self.y2 = ""
        self.z2 = ""
        self.replacement_done = False
        self.replacement_position = None  
        self.selected_uniterm_id = None  
        self.db = DataBaseManager(
            host="localhost",
            dbname="unitermdb",
            user="unitermuser",
            password="unitermpass",
            port=5433
        )
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(220)
        self.list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        main_layout.addWidget(self.list_widget)

        self.drawing_widget = UnitermDrawing()
        self.drawing_widget.setMinimumWidth(400)
        main_layout.addWidget(self.drawing_widget)

        right_panel = QWidget()
        right_panel.setObjectName("RightPanel")
        right_panel.setFixedWidth(300)
        right_layout = QVBoxLayout()

        self.input_widget = UnitermInputWidget()
        right_layout.addWidget(self.input_widget)

        self.input_widget.x1_input.textChanged.connect(self.update_variables)
        self.input_widget.y1_input.textChanged.connect(self.update_variables)
        self.input_widget.z1_input.textChanged.connect(self.update_variables)
        self.input_widget.x2_input.textChanged.connect(self.update_variables)
        self.input_widget.y2_input.textChanged.connect(self.update_variables)
        self.input_widget.z2_input.textChanged.connect(self.update_variables)

        self.btn_zamiana = QPushButton("Zamiana")
        self.btn_zamiana.clicked.connect(self.open_replacement_dialog)
        right_layout.addWidget(self.btn_zamiana)

    
        self.btn_update = QPushButton("Aktualizuj")
        self.btn_update.clicked.connect(self.handle_update_item)
        right_layout.addWidget(self.btn_update)

        right_layout.addStretch(1)

        add_box = QFrame()
        add_box.setFrameShape(QFrame.StyledPanel)
        add_layout = QVBoxLayout()
        add_layout.setContentsMargins(8, 8, 8, 8)

        self.add_name_input = QLineEdit()
        self.add_name_input.setPlaceholderText("Nazwa")
        add_layout.addWidget(self.add_name_input)

        self.add_desc_input = QLineEdit()
        self.add_desc_input.setPlaceholderText("Opis")
        add_layout.addWidget(self.add_desc_input)

        self.btn_add = QPushButton("Dodaj")
        self.btn_add.clicked.connect(self.handle_add_item)
        add_layout.addWidget(self.btn_add)

        add_box.setLayout(add_layout)
        right_layout.addWidget(add_box)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        self.setLayout(main_layout)

        self.apply_styles()
        self.load_database_items()
        self.update_variables()

    def update_variables(self):
        self.x1 = self.input_widget.x1_input.text()
        self.y1 = self.input_widget.y1_input.text()
        self.z1 = self.input_widget.z1_input.text()
        self.x2 = self.input_widget.x2_input.text()
        self.y2 = self.input_widget.y2_input.text()
        self.z2 = self.input_widget.z2_input.text()
        self.drawing_widget.update_variables(
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
            self.replacement_done,
            self.replacement_position
        )

    def open_replacement_dialog(self):
      
        if not all([self.x1, self.y1, self.z1, self.x2, self.y2, self.z2]):
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Błąd",
                "Proszę wypełnić wszystkie pola (x1, y1, z1, x2, y2, z2) przed wykonaniem operacji zamiany."
            )
            return
        
        
        dialog = ReplacementDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            selected_variable = dialog.get_selected_variable()
            self.perform_replacement(selected_variable)

    def perform_replacement(self, selected_variable):
        if selected_variable not in ("x1", "y1"):
            return
        self.replacement_done = True
        self.replacement_position = selected_variable
        print(f"Zamiana wykonana: {selected_variable} -> uniterm 2")
        print(f"Status zamiany: {self.replacement_done}")
        print(f"Pozycja zamiany: {self.replacement_position}")
        self.drawing_widget.update_variables(
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
            self.replacement_done,
            self.replacement_position
        )

    def handle_add_item(self):
        name = self.add_name_input.text().strip()
        desc = self.add_desc_input.text().strip()
        if not name:
            
            QMessageBox.warning(self, "Błąd", "Nazwa nie może być pusta.")
            return
     
        self.db.add_uniterm(
            name, desc,
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
            self.replacement_done,
            self.replacement_position
        )
        self.load_database_items()
        self.add_name_input.clear()
        self.add_desc_input.clear()

    def handle_update_item(self):
        
        if self.selected_uniterm_id is None:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Błąd", "Najpierw wybierz uniterm do aktualizacji (przycisk 👁️).")
            return
        name = self.add_name_input.text().strip()
        desc = self.add_desc_input.text().strip()
        if not name:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Błąd", "Nazwa nie może być pusta.")
            return
        self.db.update_uniterm(
            self.selected_uniterm_id,
            name, desc,
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
            self.replacement_done,
            self.replacement_position
        )
        self.load_database_items()

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
                border: none;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
                transition: background 0.2s;
            }

            QPushButton:hover {
                background-color: #005fa3;
            }

            QPushButton:pressed {
                background-color: #004c82;
            }

            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 6px;
            }

            QListWidget {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 6px;
            }

            /* Prawy panel */
            QWidget#RightPanel {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 6px;
            }
        """)

    def load_database_items(self):
        items = self.db.get_uniterms()
        self.list_widget.clear()
        for item in items:
            name = item[1] or f"Uniterm {item[0]}"
            desc = item[2] or ""
            def on_show(checked=False, item=item):
                self.selected_uniterm_id = item[0]
                self.input_widget.x1_input.setText(item[3])
                self.input_widget.y1_input.setText(item[4])
                self.input_widget.z1_input.setText(item[5])
                self.input_widget.x2_input.setText(item[6])
                self.input_widget.y2_input.setText(item[7])
                self.input_widget.z2_input.setText(item[8])
                self.replacement_done = item[9]
                self.replacement_position = item[10]
                self.add_name_input.setText(item[1] or "")
                self.add_desc_input.setText(item[2] or "")
                self.update_variables()
            def on_delete(checked=False, item=item):
                self.db.delete_uniterm(item[0])
                self.load_database_items()
            widget = DatabaseItemWidget(f"{name} ({desc})", on_show, on_delete)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, widget)

    def closeEvent(self, event):
        self.db.close()
        event.accept()

class UnitermDrawing(QWidget):
    def __init__(self):
        super().__init__()
        self.x1 = ""
        self.y1 = ""
        self.z1 = ""
        self.x2 = ""
        self.y2 = ""
        self.z2 = ""
        self.replacement_done = False
        self.replacement_position = None
        self.show_elimination_1 = False
        self.show_elimination_2 = False
        self.show_replacement = False
        self.setMinimumHeight(400)

    def update_variables(self, x1, y1, z1, x2, y2, z2, replacement_done=False, replacement_position=None):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.replacement_done = replacement_done
        self.replacement_position = replacement_position
        self.show_elimination_1 = bool(x1 and y1 and z1)
        self.show_elimination_2 = bool(x2 and y2 and z2)
        self.show_replacement = bool(replacement_done and replacement_position)
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
        

        painter.setPen(QPen(Qt.black, 1))

        if self.show_elimination_1:
            self.draw_operation(painter, start_x, start_y, self.x1, self.y1, self.z1)

        if self.show_elimination_2:
            self.draw_operation(painter, start_x, start_y + spacing, self.x2, self.y2, self.z2)

        if self.show_replacement:
        
            inserted_uniterm = {'x': self.x2, 'y': self.y2, 'z': self.z2}
            if self.replacement_position == "x1":
                result_x = inserted_uniterm
                result_y = self.y1
                result_z = self.z1
            elif self.replacement_position == "y1":
                result_x = self.x1
                result_y = inserted_uniterm
                result_z = self.z1
            else:
                result_x = self.x1
                result_y = self.y1
                result_z = self.z1
            self.draw_replacement_operation(painter, start_x, start_y + 2 * spacing, result_x, result_y, result_z)

    def draw_operation(self, painter, x, y, term1, term2, term3):
        term_text = f"{term1} ; {term2} ; {term3}"
        font_metrics = QFontMetrics(painter.font())
        text_width = font_metrics.horizontalAdvance(term_text)
        margin = 12
        line_length = text_width + 2 * margin  # Dynamiczna długość
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x, y, x + line_length, y)
        painter.drawLine(x, y - 12, x, y + 12)
        painter.drawLine(x + line_length, y - 12, x + line_length, y + 12)
        painter.setPen(QPen(Qt.black, 1))
        term_y = y + 25
        text_x = x + margin
        painter.drawText(text_x, term_y, term_text)

    def draw_replacement_operation(self, painter, x, y, term1, term2, term3):
        font_metrics = QFontMetrics(painter.font())
        terms = [term1, term2, term3]
        term_positions = []
        current_x = x + 12
        for i, term in enumerate(terms):
            if isinstance(term, dict):
                inserted_text = f"{term['x']} ; {term['y']} ; {term['z']}"
                width = font_metrics.horizontalAdvance(inserted_text) + 24
                term_positions.append({'type': 'inserted', 'x': current_x, 'width': width, 'text': inserted_text})
                current_x += width
            else:
                text = str(term)
                width = font_metrics.horizontalAdvance(text)
                term_positions.append({'type': 'normal', 'x': current_x, 'width': width, 'text': text})
                current_x += width
            if i < len(terms) - 1:
                separator = " ; "
                current_x += font_metrics.horizontalAdvance(separator)
        total_width = current_x - x
        line_length = max(total_width, 200)
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x, y, x + line_length, y)
        painter.drawLine(x, y - 12, x, y + 12)
        painter.drawLine(x + line_length, y - 12, x + line_length, y + 12)
        current_x = x + 12
        text_y = y + 25
        for i, (term, pos_info) in enumerate(zip(terms, term_positions)):
            if pos_info['type'] == 'inserted':
                uniterm_y = text_y - 15
                uniterm_width = pos_info['width']
                painter.setPen(QPen(Qt.black, 2))
                painter.drawLine(current_x, uniterm_y, current_x + uniterm_width, uniterm_y)
                painter.drawLine(current_x, uniterm_y - 6, current_x, uniterm_y + 6)
                painter.drawLine(current_x + uniterm_width, uniterm_y - 6, current_x + uniterm_width, uniterm_y + 6)
                painter.setPen(QPen(Qt.black, 1))
                painter.drawText(current_x + 12, uniterm_y + 15, pos_info['text'])
                current_x += uniterm_width
            else:
                painter.setPen(QPen(Qt.black, 1))
                painter.drawText(current_x, text_y, pos_info['text'])
                current_x += pos_info['width']
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
        description = QLabel("Wybierz wartość która ma być zamieniona:")
        layout.addWidget(description)
        self.button_group = QButtonGroup()
        self.x1_radio = QRadioButton("x1 (podstaw cały uniterm 2)")
        self.y1_radio = QRadioButton("y1 (podstaw cały uniterm 2)")
        self.x1_radio.setChecked(True)
        self.button_group.addButton(self.x1_radio)
        self.button_group.addButton(self.y1_radio)
        layout.addWidget(self.x1_radio)
        layout.addWidget(self.y1_radio)
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

class DatabaseItemWidget(QWidget):
    def __init__(self, name, on_show, on_delete):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(name)
        layout.addWidget(self.label)
        layout.addStretch(1)
        self.btn_show = QPushButton("👁️")
        self.btn_show.setToolTip("Wyświetl")
        self.btn_show.setFixedSize(32, 32)
        self.btn_show.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 18px;
                padding: 0 6px;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
        """)
        self.btn_show.clicked.connect(on_show)
        self.btn_delete = QPushButton("🗑️")
        self.btn_delete.setToolTip("Usuń")
        self.btn_delete.setFixedSize(32, 32)
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 18px;
                padding: 0 6px;
            }
            QPushButton:hover {
                background: #ffeaea;
            }
        """)
        self.btn_delete.clicked.connect(on_delete)
        layout.addWidget(self.btn_show)
        layout.addWidget(self.btn_delete)
        self.setLayout(layout)

class UnitermInputWidget(QWidget):
    """
    Widget do wprowadzania i edycji wartości x1, y1, z1, x2, y2, z2, nazwy i opisu.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Uniterm 1
        op1_layout = QVBoxLayout()
        x1_row = QHBoxLayout()
        x1_row.addWidget(QLabel("x1:"))
        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText("Wpisz wartość")
        x1_row.addWidget(self.x1_input)
        op1_layout.addLayout(x1_row)

        y1_row = QHBoxLayout()
        y1_row.addWidget(QLabel("y1:"))
        self.y1_input = QLineEdit()
        self.y1_input.setPlaceholderText("Wpisz wartość")
        y1_row.addWidget(self.y1_input)
        op1_layout.addLayout(y1_row)

        z1_row = QHBoxLayout()
        z1_row.addWidget(QLabel("z1:"))
        self.z1_input = QLineEdit()
        self.z1_input.setPlaceholderText("Wpisz wartość")
        z1_row.addWidget(self.z1_input)
        op1_layout.addLayout(z1_row)

        # Uniterm 2
        op2_layout = QVBoxLayout()
        x2_row = QHBoxLayout()
        x2_row.addWidget(QLabel("x2:"))
        self.x2_input = QLineEdit()
        self.x2_input.setPlaceholderText("Wpisz wartość")
        x2_row.addWidget(self.x2_input)
        op2_layout.addLayout(x2_row)

        y2_row = QHBoxLayout()
        y2_row.addWidget(QLabel("y2:"))
        self.y2_input = QLineEdit()
        self.y2_input.setPlaceholderText("Wpisz wartość")
        y2_row.addWidget(self.y2_input)
        op2_layout.addLayout(y2_row)

        z2_row = QHBoxLayout()
        z2_row.addWidget(QLabel("z2:"))
        self.z2_input = QLineEdit()
        self.z2_input.setPlaceholderText("Wpisz wartość")
        z2_row.addWidget(self.z2_input)
        op2_layout.addLayout(z2_row)

        layout.addLayout(op1_layout)
        layout.addSpacing(30)
        layout.addLayout(op2_layout)
        layout.addSpacing(30)

    

        self.setLayout(layout)