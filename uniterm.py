import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTextEdit, QPushButton, QVBoxLayout,
    QLabel, QDialog, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont



class EliminacjaDialog(QDialog):
    def __init__(self, callback):
        super().__init__()
        self.setWindowTitle("Eliminacja")
        self.callback = callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.result_input = QLineEdit()

        layout.addWidget(QLabel("Wyrażenie A:"))
        layout.addWidget(self.a_input)
        layout.addWidget(QLabel("Wyrażenie B:"))
        layout.addWidget(self.b_input)
        layout.addWidget(QLabel("Wyrażenie:"))
        layout.addWidget(self.result_input)

        add_btn = QPushButton("Dodaj")
        add_btn.clicked.connect(self.add_expression)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    def add_expression(self):
        a = self.a_input.text().strip()
        b = self.b_input.text().strip()
        c = self.result_input.text().strip()

        if not (a and b and c):
            QMessageBox.warning(self, "Błąd", "Wypełnij wszystkie pola!")
            return

        content = f"{a}, {b}, {c}"
        line = "─" * (len(content) + 4)
        zapis = f"├{line}┤\n   {content}"

        self.callback(a, b, c, zapis)
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uniterm PyQt")
        self.setGeometry(200, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Courier", 14)) 

        self.eliminacja_button = QPushButton("Eliminacja")
        self.eliminacja_button.clicked.connect(self.open_eliminacja)

        layout.addWidget(self.text_display)
        layout.addWidget(self.eliminacja_button)

        central_widget.setLayout(layout)

    def open_eliminacja(self):
        dialog = EliminacjaDialog(self.handle_eliminacja)
        dialog.exec_()

    def handle_eliminacja(self, a, b, c, zapis):
        self.text_display.append(zapis)
        self.save_to_db(a, b, c, zapis)

   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
