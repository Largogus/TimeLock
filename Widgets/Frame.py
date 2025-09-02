from PySide6.QtWidgets import QFrame, QHBoxLayout


class BaseFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.mainLayout = QHBoxLayout()
        self.setStyleSheet('''
            QFrame {
                background-color: #CFCFCF;
                border-radius: 10px;
            }
        ''')

        self.setLayout(self.mainLayout)

    def addButton(self, btn):
        self.mainLayout.addWidget(btn)