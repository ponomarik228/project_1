'''
ПЛАН ТОЛЬКО ДЛЯ ТИХОНА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
НЕ ЛЕЗЬТЕ, СУКИ!!!!!!!!!!!!!!!!!

1. Адаптировать окно решения, подсказку
2. Сделать об авторах, доделать подсказку
3. Сделать "посмотреть решение"
'''

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QSlider,
    QLineEdit, QDialog, QGridLayout, 
    QStackedLayout, QFrame, QGraphicsDropShadowEffect, 
    QStyleOptionSlider
)
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QEasingCurve, QTimer, QRectF, QRect
from PySide6.QtGui import QPainter, QFontDatabase, QFont, QPixmap, QColor, QBrush, QPen, QIntValidator, QDoubleValidator

import sys
import os
from random import randint, random

app = QApplication([])
QFontDatabase.addApplicationFont("ProjUITest/Assets/UI_FONT.otf")
QFontDatabase.addApplicationFont("ProjUITest/Assets/TEXT_FONT.ttf")
QFontDatabase.addApplicationFont("ProjUITest/Assets/SegoePro-Semibold.ttf")

# ---------------- РАЗМЕР ЭКРАНА ----------------
def get_scale(screen_size, base_resolution=(1280, 720)):
    scale_w = screen_size.width() / base_resolution[0]
    scale_h = screen_size.height() / base_resolution[1]
    return int(min(scale_w, scale_h))

# ---------------- АДАПТИВНЫЕ КНОПКИ ----------------
def generate_adaptive_qss(button, 
                          base_size=(570, 90),
                          base_font=37,
                          base_padding=(15, 30),
                          base_border_radius=20,
                          base_border_width=2,
                          border_color="#111111",
                          hover_scale=1.3,
                          hover_border_multiplier=1.8,
                          enlarge_on_hover=False,
                          thicker_border_on_hover=True):
    """
    Генерирует QSS и задает размеры кнопки пропорционально экрану.
    enlarge_on_hover — увеличивать кнопку при hover
    thicker_border_on_hover — утолщать рамку при hover
    """
    scale = get_scale(button.screen().size())

    # размеры кнопки
    w = int(base_size[0] * scale)
    h = int(base_size[1] * scale)
    button.setFixedSize(w, h)

    # шрифт
    font = QFont()
    font.setPointSize(int(base_font * scale))
    font.setBold(True)
    button.setFont(font)

    # padding, border-radius, border-width
    pad_v = int(base_padding[0] * scale)
    pad_h = int(base_padding[1] * scale)
    border_radius = int(base_border_radius * scale)
    border_width = max(int(base_border_width * scale), 1)
    hover_border = max(int(border_width * hover_border_multiplier), 1)

    # формируем QSS
    qss = f"""
    QPushButton {{
        border: {border_width}px solid {border_color};
        border-radius: {border_radius}px;
        padding: {pad_v}px {pad_h}px;
    }}
    """

    # hover эффекты
    hover_styles = ""
    if enlarge_on_hover:
        hover_styles += f"font-size: {int(base_font * scale * hover_scale)}px;"
    if thicker_border_on_hover:
        hover_styles += f"border-width: {hover_border}px;"

    if hover_styles:
        qss += f"""
        QPushButton:hover {{
            {hover_styles}
        }}
        """

    button.setStyleSheet(qss)

# ---------------- ТЕКСТ - ХУД ----------------
def create_corner_label(text, scale, size):
    label = QLabel(text)
    label.setObjectName("textUI")
    label.setAlignment(Qt.AlignCenter)

    font = label.font()
    font.setPointSize(int(size * scale))
    label.setFont(font)

    return label

# ---------------- ЛОГО+ТЕКСТ - ХУД ----------------
class CornerWidget(QWidget):
    def __init__(
        self,
        top_right_text="",
        show_bottom=False,
        bottom_left_text="",
        bottom_right_text="",
        font_size=17
    ):
        super().__init__()

        layout = QGridLayout(self)

        scale = get_scale(self.screen().size())
        margin = int(20 * scale)

        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(0)

        # --- ЛОГО ---
        logo = QLabel()
        pixmap = QPixmap("ProjUITest/Assets/logo.png")

        size = int(50 * scale)
        logo.setPixmap(
            pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        layout.addWidget(logo, 0, 0, alignment=Qt.AlignLeft | Qt.AlignTop)

        # --- ВЕРХНИЙ ПРАВЫЙ ТЕКСТ ---
        if top_right_text:
            label = create_corner_label(top_right_text, scale, font_size)
            layout.addWidget(label, 0, 1, alignment=Qt.AlignRight | Qt.AlignTop)

        # --- НИЖНИЕ (если нужны) ---
        if show_bottom:
            if bottom_left_text:
                bl = create_corner_label(bottom_left_text, scale, font_size)
                layout.addWidget(bl, 1, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)

            if bottom_right_text:
                br = create_corner_label(bottom_right_text, scale, font_size)
                layout.addWidget(br, 1, 1, alignment=Qt.AlignRight | Qt.AlignBottom)

# ---------------- МЕНЮ ----------------
class MainMenu(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Основной лейаут
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Фон — CornerWidget (занимает всё пространство)
        self.corner = CornerWidget(
            top_right_text="ПРОЕКТНАЯ РАБОТА — 2026",
            show_bottom=True,
            bottom_left_text="ВЕРСИЯ 1.0.0",
            bottom_right_text="ГОТОВО К РАБОТЕ!"
        )
        main_layout.addWidget(self.corner)

        # Контейнер для кнопок (накладывается поверх фона)
        self.button_overlay = QFrame(self)
        self.button_overlay.setStyleSheet("background: transparent;")
        self.button_overlay.setFrameStyle(QFrame.NoFrame)

        # Лейаут для кнопок внутри overlay
        button_layout = QVBoxLayout(self.button_overlay)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Кнопка «РЕШИТЬ ЗАДАЧУ!»
        self.main_btn = QPushButton("РЕШИТЬ ЗАДАЧУ!", self.button_overlay)
        self.main_btn.setObjectName("mainButton")
        button_layout.addWidget(self.main_btn, alignment=Qt.AlignCenter)

        generate_adaptive_qss(
            self.main_btn, 
            base_border_width=1,
            border_color="#111111",
            enlarge_on_hover=True,
            thicker_border_on_hover=False)
        
        # ДОБАВЛЯЕМ ЦВЕТ ФОНА
        self.main_btn.setStyleSheet(
        self.main_btn.styleSheet() +
        "QPushButton#mainButton { background-color: #111111; color: white; }")


        # Кнопка «О ПРОГРАММЕ»
        self.about_btn = QPushButton("О ПРОГРАММЕ", self.button_overlay)
        self.about_btn.setObjectName("secondaryButton")
        button_layout.addWidget(self.about_btn, alignment=Qt.AlignCenter)
        generate_adaptive_qss(
            self.about_btn,
            base_size=(280, 57),
            base_font=20,
            base_padding=(8, 20),
            base_border_radius=17,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True
        )


        # Кнопка «ВЫХОД»
        self.exit_btn = QPushButton("ВЫХОД", self.button_overlay)
        self.exit_btn.setObjectName("secondaryButton")
        button_layout.addWidget(self.exit_btn, alignment=Qt.AlignCenter)
        generate_adaptive_qss(
            self.exit_btn,
            base_size=(280, 57),
            base_font=20,
            base_padding=(8, 20),
            base_border_radius=17,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True
        )

        # --- Overlay изображение ---
        self.overlay = QLabel(self)
        self.overlay.setPixmap(QPixmap("ProjUITest/Assets/overlay.png"))
        self.overlay.setScaledContents(True)  # растягиваем под размер окна
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)  # чтобы не блокировало клики
        self.overlay.raise_()  # поднимаем поверх всех виджетов

    def resizeEvent(self, event):
        # При изменении размера окна растягиваем overlay на всё пространство
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.button_overlay.resize(self.size())
        super().resizeEvent(event)

        # навигация
        self.main_btn.clicked.connect(lambda: self.app.go(2))
        self.about_btn.clicked.connect(lambda: self.app.go(1))
        self.exit_btn.clicked.connect(self.app.close)

# ---------------- О ПРОГРАММЕ ----------------
class AboutPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("О ПРОГРАММЕ")
        title.setObjectName("title")
        layout.addWidget(title)

        text = QLabel(
            "Программа предназначена для решения задачи.\n"
            "Позволяет вводить параметры и получать результат."
        )
        text.setWordWrap(True)
        layout.addWidget(text)

        authors = QLabel("ОБ АВТОРАХ\n\nИванов\nПетров\nСидоров")
        layout.addWidget(authors)

        layout.addStretch()

        back = QPushButton("НАЗАД")
        layout.addWidget(back, alignment=Qt.AlignRight)

        back.clicked.connect(lambda: self.app.go(0))

# ---------------- ГРАФИК ----------------
class GraphWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)

        # оси
        painter.drawLine(40, 200, 300, 200)
        painter.drawLine(40, 200, 40, 40)

        # линия (пример)
        painter.drawLine(40, 200, 250, 100)

# ---------------- ПОДСКАЗКА ----------------
class HintDialog(QDialog):
    def __init__(self):
        super().__init__()

        #убираем рамку винды
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        #прозрачность окна
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(500, 650)

        # главный layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- карточка ---
        self.card = QWidget(self)
        self.card.setObjectName("card")

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)

        # заголовок
        title = QLabel("ПОДСКАЗКА")
        title.setObjectName("title")

        # текст
        text = QLabel(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
        )
        text.setWordWrap(True)
        text.setObjectName("text")

        # кнопка
        btn = QPushButton("ПОСМОТРЕТЬ РЕШЕНИЕ")

        # крестик
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)

        card_layout.addWidget(close_btn, alignment=Qt.AlignRight)
        card_layout.addWidget(title)
        card_layout.addWidget(text)
        card_layout.addStretch()
        card_layout.addWidget(btn)

        layout.addWidget(self.card, alignment=Qt.AlignCenter)

        # стиль
        self.setStyleSheet("""
            QDialog#card {
                background-color: rgba(0, 0, 0, 235);
                border-radius: 20px;
            }

            QLabel#title {
                font-size: 32px;
                color: white;
                font-weight: bold;
            }

            QLabel#text {
                font-size: 16px;
                color: white;
            }

            QPushButton {
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
            }
        """)

        # для перетаскивания
        self.drag_pos = None

    # затемнение фона
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 235))  # затемнение

    # --- перетаскивание ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.pos() + delta)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

# ---------------- СЛАЙДЕР СТРОКА ----------------
class Slider(QWidget):
    def __init__(self,
                 unit_label = '',
                 label = ''):
        super().__init__()

        self.min_value = 0
        self.max_value = 100
        scale = get_scale(self.screen().size()) 

        # === Левый текст ===
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        qss_1 = f"""
        QLabel {{
            font-size: {20*scale}px;
            font-family: Gerhaus;
        }}
        """
        self.label.setStyleSheet(qss_1)

        # === Слайдер ===
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(self.min_value, self.max_value)
        self.slider.setValue(randint(0, 100))  ###МОЖНО УБРАТЬ РАНДОМ, А МОЖНО ОСТАВИТЬ. ДОБАВЛЕН ДЛЯ ВАЙБА!!!
        self.slider.setMinimumHeight(40*scale)
        self.slider.setFixedWidth(350*scale)

        # === Капсула ===
        self.input = QLineEdit()
        self.input.setFixedSize(80*scale, 30*scale)
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setValidator(QIntValidator())
        self.input.setText(str(self.slider.value()))

        # === Единица измерения ===
        self.unit_label = QLabel(unit_label)
        qss_2 = f"""
        QLabel {{
            font-size: {17*scale}px;
            font-family: Gerhaus;
        }}
        """
        self.unit_label.setStyleSheet(qss_2)

        # === Стили input ===
        qss_3 = f"""
        QLineEdit {{
            border-radius: {10*scale}px;
            background: transparent;
            border: {3*scale}px solid #111111;
            font-size: {20*scale}px;
            font-family: Gerhaus;
        }}
        """
        self.input.setStyleSheet(qss_3)

        # === Стили slider ===
        qss_4 = f"""
        QSlider::groove:horizontal {{
            height: {11*scale}px;
            background: transparent;
            border-radius: {8*scale}px;
            border: {3*scale}px solid #111111;
            margin-left: {5*scale}px;
            margin-right: {11*scale}px;
        }}
        QSlider::sub-page:horizontal {{
            background: #111111;
            border-radius: {8*scale}px;
        }}

        QSlider::add-page:horizontal {{
            background: transparent;
            border-radius: {8*scale}px;
            margin: 0px;
        }}

        QSlider::handle:horizontal {{
            background: #111111;
            width: {22*scale}px;
            height: {22*scale}px;
            border-radius: {11*scale}px;
            margin: {-6*scale}px {-3*scale}px;
            border: none;
        }}

        """
        self.slider.setStyleSheet(qss_4)

        # === Layout ===
        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        top_layout.addWidget(self.label)
        top_layout.addStretch()

        bottom_layout.addWidget(self.slider)
        bottom_layout.addSpacing(-1*scale)
        bottom_layout.addWidget(self.input)
        bottom_layout.addSpacing(-1*scale)
        bottom_layout.addWidget(self.unit_label)

        main_layout.addLayout(top_layout)
        main_layout.addSpacing(-10*scale)
        main_layout.addLayout(bottom_layout)

        # === Связка ===
        self.slider.valueChanged.connect(self.on_slider_change)
        self.input.editingFinished.connect(self.on_input_change)

        self.setFixedHeight(67*scale)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(13,0,0,5)

    def on_slider_change(self, value):
        if self.input.text() != str(value):
            self.input.setText(str(value))

    def on_input_change(self):
        text = self.input.text()
        value = int(text)
        

        value = max(self.min_value, min(value, self.max_value))
        self.slider.setValue(value)

# ---------------- КАСТОМНАЯ ПАНЕЛЬ ----------------  
class CastomPanel(QWidget):
    def __init__(self, radius=20,border_width=3):
        super().__init__()

        self.radius = radius
        self.border_width = border_width
        self.border_color = '#111111'

        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(
            self.border_width,
            self.border_width,
            -self.border_width,
            -self.border_width
        )

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(self.border_width)
        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawRoundedRect(rect, self.radius, self.radius)

# ---------------- ПАНЕЛЬ ВВОДА ЗН-Й ----------------
class input_panel(CastomPanel):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)


        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10,10,10,10)

        self.sliders = {}
        label_dict = {"P_пл": "Н", "AB": "см", "OA": "см", "OC": "см", "P": "Н", }

        for key in label_dict:
            slider = Slider(label_dict[key], key)  # создаём
            self.sliders[key] = slider             # сохраняем
            layout.addWidget(slider)
            layout.setSpacing(-20)

        layout.setSpacing(35)

        btn_row = QHBoxLayout()
        self.reset_btn = QPushButton("СБРОСИТЬ")
        self.reset_btn.setObjectName("secondaryButton")
        generate_adaptive_qss(
            self.reset_btn,
            base_size=(200, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True
        )

        self.random_btn = QPushButton("СЛУЧАЙНЫЕ ЗН-Я")
        self.random_btn.clicked.connect(lambda: self.set_value("P_пл", 1)) # написать ф-ю рандомизации зн-й, запихнуть сюда
        self.random_btn.setObjectName("mainButton")
        generate_adaptive_qss(
            self.random_btn,
            base_size=(270, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True,
            thicker_border_on_hover=False
        )
        self.random_btn.setStyleSheet(
        self.random_btn.styleSheet() +
        "QPushButton#mainButton { background-color: #111111; color: white; }")
        btn_row.addWidget(self.reset_btn)
        btn_row.setSpacing(10)
        btn_row.addWidget(self.random_btn)

        layout.addLayout(btn_row)
    
    #получить значение с слайдера
    def get_value(self, key):
        return self.sliders[key].slider.value()
        
    #изменить значение слайдера
    def set_value(self, key, value):
        self.sliders[key].slider.setValue(value)
        #self.sliders[str(value)].input.setText(str(value))

# ---------------- ПОЛЕ ВВОДА ----------------
class answer_panel(QWidget):
    def __init__(self,
                 unit_label = '',
                 label = ''):
        super().__init__()

        scale = get_scale(self.screen().size()) 

        # === Левый текст ===
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        qss_1 = f"""
        QLabel {{
            font-size: {20*scale}px;
            font-family: Gerhaus;
        }}
        """
        self.label.setStyleSheet(qss_1)

        # === Капсула ===
        self.input = QLineEdit()
        self.input.setFixedSize(80*scale, 30*scale)
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setValidator(QDoubleValidator())
        self.input.setText(str(round(random(), 2)))  ###УБРАТЬ РАНДОМ, ДОБАВЛЕН ДЛЯ ВАЙБА!!!

        # === Единица измерения ===
        self.unit_label = QLabel(unit_label)
        qss_2 = f"""
        QLabel {{
            font-size: {17*scale}px;
            font-family: Gerhaus;
        }}
        """
        self.unit_label.setStyleSheet(qss_2)

        # === Стили input ===
        qss_3 = f"""
        QLineEdit {{
            border-radius: {10*scale}px;
            background: transparent;
            border: {3*scale}px solid #111111;
            font-size: {20*scale}px;
            font-family: Gerhaus;
        }}
        """
        self.input.setStyleSheet(qss_3)

        # === Layout ===
        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        top_layout.addWidget(self.label)
        top_layout.addStretch()

        bottom_layout.addWidget(self.input)
        bottom_layout.addSpacing(-1*scale)
        bottom_layout.addWidget(self.unit_label)

        main_layout.addLayout(top_layout)
        main_layout.addSpacing(-5*scale)
        main_layout.addLayout(bottom_layout)

        self.setFixedHeight(60*scale)
        #main_layout.setSpacing(2)
        main_layout.setContentsMargins(28,0,0,3)

# ---------------- ПАНЕЛЬ РЕЗУЛЬТАТА ----------------
class result_panel(CastomPanel):
    def __init__(self):
        super().__init__()

        scale = get_scale(self.screen().size()) 

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.values = {}

        values_layout = QHBoxLayout()

        label_dict = {"X_0": "Н", "Y_0": "H", "Y_C": "H"}

        for key in label_dict:
            value_ans = answer_panel(label_dict[key], key)  # создаём
            self.values[key] = value_ans             # сохраняем
            values_layout.addWidget(value_ans)
            values_layout.setSpacing(-5)

        layout.addLayout(values_layout)

        # КНОПКИ
        btn_row = QHBoxLayout()

        self.reset_btn = QPushButton("СБРОСИТЬ")
        self.reset_btn.clicked.connect(lambda: self.set_value_ans('X_0', 0)) # ну почти, только для троих сделать, желательно отдельной ф-й
        self.reset_btn.setObjectName("secondaryButton")
        generate_adaptive_qss(
            self.reset_btn,
            base_size=(200, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True
        )
        self.check_btn = QPushButton("ПРОВЕРИТЬ ОТВЕТ")
        self.check_btn.clicked.connect(lambda: print(self.get_value_ans('X_0')))  # просто для примера, переделать
        self.check_btn.setObjectName("mainButton")
        generate_adaptive_qss(
            self.check_btn,
            base_size=(270, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True,
            thicker_border_on_hover=False
        )

        self.check_btn.setStyleSheet(
        self.check_btn.styleSheet() +
        "QPushButton#mainButton { background-color: #111111; color: white; }")
        btn_row.addWidget(self.reset_btn)
        btn_row.setSpacing(-5)
        btn_row.addWidget(self.check_btn)

        layout.addLayout(btn_row)

    #получить значение с поля ввода
    def get_value_ans(self, key):
        return float(self.values[key].input.text())
        
        #изменить значение поля ввода
    def set_value_ans(self, key, value):
        self.values[key].input.setText(str(value))

# ---------------- ОСНОВНОЙ ЭКРАН ----------------
class SolverPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.corner = CornerWidget(
            top_right_text="РЕШЕНИЕ ЗАДАЧИ",
            show_bottom=False,
        )
        main_layout.addWidget(self.corner)

        # Контейнер всего (накладывается поверх фона)
        self.all_overlay = QFrame(self)
        self.all_overlay.setStyleSheet("background: transparent;")
        self.all_overlay.setFrameStyle(QFrame.NoFrame)

        # Лейаут всего внутри overlay
        all_layout = QHBoxLayout(self.all_overlay)
        #all_layout.setAlignment(Qt.AlignCenter)
        all_layout.setContentsMargins(20, 70, 20, 15)
        all_layout.setSpacing(20)

        # ---- ЛЕВАЯ ПАНЕЛЬ ----
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.input_panel = input_panel()
        self.result_panel = result_panel()

        left_layout.addWidget(self.input_panel)
        left_layout.addWidget(self.result_panel)
        left_layout.addStretch()

        #all_layout.addWidget(left_widget)

        # ---- ПРАВАЯ ПАНЕЛЬ ----
        right_widget = QWidget()
        right = QVBoxLayout(right_widget)

        self.graph = GraphWidget()
        self.graph.setMinimumHeight(250)

        right.addWidget(self.graph)

        btns = QVBoxLayout()

        self.hint = QPushButton("ПОДСКАЗКА")
        self.hint.setObjectName("secondaryButton")
        generate_adaptive_qss(
            self.hint,
            base_size=(200, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True
        )
        self.back = QPushButton("НАЗАД")
        self.back.setObjectName("secondaryButton")
        generate_adaptive_qss(
            self.back,
            base_size=(200, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            enlarge_on_hover=True
        )

        btns.addWidget(self.hint)
        btns.addWidget(self.back)

        btns.setAlignment(Qt.AlignRight)

        right.addLayout(btns)

        all_layout.addWidget(left_widget, 1)
        all_layout.addWidget(right_widget, 2)
        #main_layout.addWidget(self.all_overlay, 0, 0)

        # действия
        self.back.clicked.connect(lambda: self.app.go(0))
        self.hint.clicked.connect(self.show_hint)

        # --- Overlay изображение ---
        self.overlay = QLabel(self)
        self.overlay.setPixmap(QPixmap("ProjUITest/Assets/overlay.png"))
        self.overlay.setScaledContents(True)  # растягиваем под размер окна
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)  # чтобы не блокировало клики
        self.overlay.raise_()  # поднимаем поверх всех виджетов

    def show_hint(self):
        dialog = HintDialog()
        dialog.exec()

    def resizeEvent(self, event):
        self.all_overlay.setGeometry(0,0,self.width(),self.height())
        super().resizeEvent(event)

# ---------------- APP ----------------
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Проект")
        self.showFullScreen()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.stack.addWidget(MainMenu(self))   # 0
        self.stack.addWidget(AboutPage(self))  # 1
        self.stack.addWidget(SolverPage(self)) # 2

    def go(self, index):
        self.stack.setCurrentIndex(index)

    
    

STYLE = """
QMainWindow {
    border-image: url("ProjUITest/Assets/bg.png") 0 0 0 0 stretch stretch; 
    
}

QPushButton#mainButton {
    font-weight: bold;               
    font-family: Gerhaus;
    color: white;
}

QPushButton#secondaryButton {
    background-color: transparent;
         
    font-family: Gerhaus;
    color: #111111;
}

QLabel#title {
    font-size: 24px;
    font-weight: bold;
}

QLabel#textUI {
    color: #111111;
    font-family: Segoe Pro;
    font-weight: bold;
    background-color: transparent;
}

QWidjet#help_window {
    background-color: rgba(0,0,0,200);
    border-radius: 20px;
}
}
"""


# ---------------- ЗАПУСК ----------------
if __name__ == "__main__":
    
    #app = QApplication([])
    app.setStyleSheet(STYLE)

    window = App()
    window.show()

    app.exec()
    

