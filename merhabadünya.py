import sys
from PyQt5.QtWidgets import QMessageBox,QGridLayout,QVBoxLayout,QHBoxLayout,QMainWindow,QWidget,QLineEdit, QPushButton
from PyQt5.QtCore import Qt
class semiconductu(QMainWindow):
    def __init__(self):
        super().__init__
        self.setFixedSize(300,400)
        self.setWindowTitle("Merhaba!")
        
        self.general = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.general)
        self.first = None
        self.Operator = None
        self.createdisplay()
        self.createbuttons()
    def createdisplay(self):
        self.display = QLineEdit()
        self.display.setFixedSize(180,35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
                                   background-color: #c6c2cc;
                                   color: #000000;
                                   font-size: 24px;
                                   font-family: "inter";
                                   border: 3px solid #ffffff;
                                   border-radius: 5px;
                                   
                                   
                                   
                                   
                                   
                                   """)
        self.general.addWidget(self.display,0,0,1,4)
    def createbuttons(self):
        buttons = {
            "1": (1,0), "2": (1,1), "3": (1,2), "+": (1,3),
            "4": (2,0), "5": (2,1), "6": (2,2), "-": (2,3),
            "7": (3,0), "8": (3,1), "9": (3,2), "X": (3,3),
            "0": (4,0), ".": (4,1), "=": (4,2), "/": (4,3),
            "C": (5,0,1,4)
        }
        classic= """
            QPushButton {
                            background-color: #eae8ed;
                            color: #0b8ee6;
                            font-weight: bold;
                            font-family: "inter";
                            border: 3px solid #000000;
                            border-radius: 5px;
                            padding: 8px;
                            }
            QPushButton:hover {

                            background-color:#a6aeb3;
                            }
            
            QPushButton:pressed {

                            background-color: #7e878c;
                            }
                            """
        operator = """



            QPushButton {

                            
                            background-color: #46cfb8;
                            color: #0b8ee6;
                            font-weight: bold;
                            font-family: "inter";
                            border: 3px solid #000000;
                            border-radius: 5px;
                            padding: 8px;
                            }
            QPushButton:hover {

                            background-color:#399183;
                            }
            
            QPushButton:pressed {

                            background-color: #256157;
                            }
                            """
            
        main = """
            QPushButton {

                            
                            background-color: #d92f1c;
                            color: #0b8ee6;
                            font-weight: bold;
                            font-family: "inter";
                            border: 3px solid #000000;
                            border-radius: 5px;
                            padding: 8px;
                            }
            QPushButton:hover {

                            background-color:#b83a2c;
                            }
            
            QPushButton:pressed {

                            background-color: #852f25;
                            }
        """
        for btn,pos in buttons.items():
            button = QPushButton(btn)
            if btn == 



















        """






                    


                    



                    





                        """











"""








        

    


