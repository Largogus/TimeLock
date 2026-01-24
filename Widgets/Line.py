from PySide6.QtWidgets import QFrame


class Line(QFrame):
    def __init__(self, box: str = 'H'):
        super().__init__()

        if box.lower() == 'h':
            self.setFrameShape(QFrame.Shape.HLine)
        else:
            self.setFrameShape(QFrame.Shape.VLine)

        self.setFrameShadow(QFrame.Shadow.Sunken)