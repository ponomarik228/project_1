from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QSize, QEasingCurve, QTimer

app = QApplication([])

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.btn = QPushButton("Главная кнопка")
        layout.addWidget(self.btn)

        # Анимация размера
        self.anim_size = QPropertyAnimation(self.btn, b"size")
        self.anim_size.setDuration(150)
        self.anim_size.setEasingCurve(QEasingCurve.OutCubic)

        # После того как layout установился, сохраняем реальный размер
        QTimer.singleShot(0, self.setup_button)

    def setup_button(self):
        self.orig_size = self.btn.size()

        # hover
        self.btn.enterEvent = lambda event: self.hover_enter()
        self.btn.leaveEvent = lambda event: self.hover_leave()

    def hover_enter(self):
        self.anim_size.stop()
        self.anim_size.setStartValue(self.btn.size())
        self.anim_size.setEndValue(QSize(int(self.orig_size.width() * 1.08),
                                         int(self.orig_size.height() * 1.08)))
        self.anim_size.start()

    def hover_leave(self):
        self.anim_size.stop()
        self.anim_size.setStartValue(self.btn.size())
        self.anim_size.setEndValue(self.orig_size)
        self.anim_size.start()

w = MainWindow()
w.show()
app.exec()

QSlider::handle:horizontal {{
            background: #111111;
            width: {22*scale}px;
            height: {22*scale}px;
            border-radius: {11*scale}px;
            margin: {-6*scale}px {-3*scale}px;
            border: none;
        }}