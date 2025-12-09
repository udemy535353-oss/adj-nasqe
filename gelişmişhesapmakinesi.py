from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, 
    QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QFont

class semicondur(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("this is a semicondur test")
        self.setFixedSize(300,400)
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.first_number = None
        self.operator = None
        self.createdisplay()
        self.createbuttons()
    def createdisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
                                   background-color: #f5f5f5;
                                   color: #000000;
                                   font-size: 24px;
                                   font-family: "inter";
                                    """)
        self.generalLayout.addWidget(self.display,0,0,1,4)
    def createbuttons(self):
        buttons = {
        
            "1": (1,0), "2": (1,1), "3": (1,2), "+": (1,3),
            "4": (2,0), "5": (2,1), "6": (2,2), "-": (2,3),
            "7": (3,0), "8": (3,1), "9": (3,2), "X": (3,3),
            "0": (4,0), ".": (4,1), "=": (4,2), "/": (4,3),
            "C": (5,0,1,4)

        }
        
        button_style = """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                background-color:  #f7faf9;
                color: #0078d4;
                border: 3px solid #000000;
                border-radius: 10px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #d4d7d9;
            }
            QPushButton:pressed {
                background-color: #aeb4b8;
            }
        """
        
        operator_style = """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                background-color: #0078d4;
                color: #ffffff;
                
                border: 3px solid #000000;
                border-radius: 5px;
                min-height: 50px;}
            QPushButton:hover {
                background-color: #154366;
            }
            QPushButton:pressed {
            background-color: #082236;
            }"""
        for btn,pos in buttons.items():
            button = QPushButton()
            button.setText(btn)
            if btn in ["+", "-", "X", "/"]:
                button.setStyleSheet(operator_style)
            else:
                button.setStyleSheet(button_style)
            button.setFont(QFont("inter", 18))
            if len(pos) > 2:
                self.generalLayout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
            else:
                self.generalLayout.addWidget(button, pos[0], pos[1])
            button.clicked.connect(self.press)
    def press(self):
        button = self.sender()
        key = button.text()
        if key.isdigit() or (key == "." and "." not in self.display.text()): 
            current = self.display.text()
            if current == 0 or current == "Hata":
                self.display.setText(key)
            else:
                self.display.setText(current + key)
        elif key in ["+", "-", "X", "/"]:
            try:
                self.first_number = float(self.display.text())
                self.operator = key
                self.display.clear()
            except :
                self.display.setText("Hata")
        elif key == "C":
            self.display.clear()
            self.first_number = None
            self.operator = None
        elif key == "=":
            self.calculate()
    def calculate(self):
        if self.first_number is None or self.operator is None:
            self.display.setText("Hata")
            return
        try:
            second_number = float(self.display.text())
            if self.operator == "+":
                result = self.first_number + second_number
            elif self.operator == "-":
                result = self.first_number - second_number
            elif self.operator == "X":
                result = self.first_number * second_number
            elif self.operator == "/":
                if second_number == 0:
                    raise ZeroDivisionError("Division by zero")
                result = self.first_number / second_number
            if result.is_integer():
                  self.display.setText(str(int(result)))
            else:
                self.display.setText(str(round(result, 8)))
        except Exception as e:
            self.display.setText("Hata")
            QMessageBox.critical(self, "Kritik Hata", f"Uygulamada beklenmeyen bir hata oluştu: {e}")
        finally:
            self.first_number = None
            self.operator = None
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #ffffff;
    }""")
    window = semicondur()
    window.show()
    sys.exit(app.exec_())