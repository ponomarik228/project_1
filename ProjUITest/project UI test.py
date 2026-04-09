'''
ПЛАН ТОЛЬКО ДЛЯ ТИХОНА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
НЕ ЛЕЗЬТЕ, СУКИ!!!!!!!!!!!!!!!!!

1. +++
2. Сделать об авторах, доделать подсказку, адаптировать ее
3. Сделать "посмотреть решение"
'''

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QSlider,
    QLineEdit, QDialog, QGridLayout, 
    QStackedLayout, QFrame, QGraphicsDropShadowEffect, 
    QStyleOptionSlider, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QEasingCurve, QTimer, QRectF, QRect, QRegularExpression
from PySide6.QtGui import QPainter, QFontDatabase, QFont, QPixmap, QColor, QBrush, QPen, QIntValidator, QDoubleValidator, QRegularExpressionValidator, QTransform

import sys
import os
from random import randint, random
from math import ceil

# ---------------- РАЗМЕР ЭКРАНА ----------------
def get_scale(screen_size, base_resolution=(1280, 720)):
    scale_w = screen_size.width() / base_resolution[0]
    scale_h = screen_size.height() / base_resolution[1]
    return min(scale_w, scale_h)

# ---------------- АДАПТИВНЫЕ КНОПКИ ----------------
def generate_adaptive_qss(button, 
                          base_size=(570, 90),
                          base_font=37,
                          base_padding=(15, 30),
                          base_border_radius=20,
                          base_border_width=2,
                          border_color="#0C0000",
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
    w = ceil(base_size[0] * scale)
    h = ceil(base_size[1] * scale)
    button.setFixedSize(w, h)

    # шрифт
    font = QFont()
    font.setPointSize(ceil(base_font * scale))
    font.setBold(True)
    button.setFont(font)

    # padding, border-radius, border-width
    pad_v = ceil(base_padding[0] * scale)
    pad_h = ceil(base_padding[1] * scale)
    border_radius = ceil(base_border_radius * scale)
    border_width = max(ceil(base_border_width * scale), 1)
    hover_border = max((border_width * hover_border_multiplier), 1)

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
        hover_styles += f"font-size: {round(base_font * scale * hover_scale)}px;"
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

        scale = get_scale(self.screen().size()) 

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
        button_layout.setSpacing(ceil(15*scale))
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Кнопка «РЕШИТЬ ЗАДАЧУ!»
        self.main_btn = QPushButton("РЕШИТЬ ЗАДАЧУ!", self.button_overlay)
        self.main_btn.setObjectName("mainButton")
        button_layout.addWidget(self.main_btn, alignment=Qt.AlignCenter)

        generate_adaptive_qss(
            self.main_btn, 
            base_border_width=1,
            border_color="#060000",
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

        authors = QLabel("ОБ АВТОРАХ\n\nПономарев\nБехтерев\nШишак")
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

        scale = get_scale(self.screen().size()) 

        #убираем рамку винды
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        #прозрачность окна
        self.setAttribute(Qt.WA_TranslucentBackground)

        #self.setFixedSize(500, 650)

        # главный layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30*scale, 30*scale, 30*scale, 30*scale)

        # --- карточка ---
        self.card = QWidget(self)
        self.card.setObjectName("card")
        self.card.setFixedSize(550*scale, 650*scale)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40*scale, 40*scale, 40*scale, 40*scale)
        card_layout.setSpacing(15*scale)

        text_layout = QVBoxLayout(self)
        text_layout.setContentsMargins(25*scale, 0, 25*scale, 25*scale)
        #text_layout.setSpacing(15)

        # заголовок
        title = QLabel("ПОДСКАЗКА")
        title.setObjectName("title")

        # текст
        text = QLabel(
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        )
        text.setWordWrap(True)
        text.setObjectName("text")

        # кнопка
        btn = QPushButton("ПОСМОТРЕТЬ РЕШЕНИЕ")
        btn.setObjectName("help_btn")
        generate_adaptive_qss(btn, 
                          base_size=(300, 47),
                          base_font=15,
                          base_padding=(6, 6),
                          base_border_radius=14,
                          base_border_width=3,
                          border_color="#F3F3F3",
                          hover_scale=1.25,
                          enlarge_on_hover=True)

        # крестик
        close_btn = QPushButton("X")
        close_btn.setObjectName("help_btn")
        generate_adaptive_qss(close_btn, 
                          base_size=(36, 36),
                          base_font=12,
                          base_padding=(1, 1),
                          base_border_radius=18,
                          base_border_width=3,
                          border_color="#F3F3F3",
                          hover_scale=1.22,
                          enlarge_on_hover=True)


        close_btn.clicked.connect(self.close)

        card_layout.addWidget(close_btn, alignment=Qt.AlignRight)

        text_layout.addWidget(title)
        text_layout.addWidget(text)

        card_layout.addLayout(text_layout)

        card_layout.addStretch()
        card_layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addWidget(self.card, alignment=Qt.AlignCenter)

        # стиль
        self.setStyleSheet(f"""
            QDialog {{
                background-color: rgba(0, 0, 0, 180);  /* Полупрозрачное затемнение всего окна */
            }}

            QWidget#card {{
                background-color: rgba(0, 0, 0, 235);  /* Тёмный фон карточки */
                border-radius: {30*scale}px;                        /* Закруглённые углы */
                margin: {20*scale}px;                             /* Отступ от краёв диалога */
            }}

            QLabel#title {{
                font-size: {60*scale}px;
                font-family: Gerhaus;
                color: white;
                font-weight: bold;
            }}

            QLabel#text {{
                font-size: {20*scale}px;
                font-family: Segoe Pro;
                color: white;
            }}
        """)

        # для перетаскивания
        self.drag_pos = None

    # затемнение фона
    '''
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 235))  # затемнение
    '''

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
                 label = '',
                 min_value = 0):
        super().__init__()

        self.min_value = min_value
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
        self.slider.setRange(min_value, self.max_value)
        self.slider.setValue(min_value) 
        self.slider.setMinimumHeight(40*scale)
        self.slider.setFixedWidth(350*scale)

        # === Капсула ===
        self.input = QLineEdit()
        self.input.setFixedSize(80*scale, 30*scale)
        self.input.setAlignment(Qt.AlignCenter)
        #self.input.setValidator(QIntValidator())

        # Создаем валидатор для дробных чисел
        regex = QRegularExpression(r"^\d+(\.\d{0,2})?$")
        validator = QRegularExpressionValidator(regex)
        self.input.setValidator(validator)
        
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
            width: {ceil(22*scale)}px;
            height: {ceil(22*scale)}px;
            border-radius: {ceil(11*scale)}px;
            margin: {ceil(-6*scale)}px {ceil(-3*scale)}px;
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
        main_layout.setSpacing(2*scale)
        main_layout.setContentsMargins(13*scale,0,0,5*scale)

    def on_slider_change(self, value):
        old = self.input.text()
        if value >= self.max_value:
            self.input.setText(str(self.max_value))
            return

        if "." not in self.input.text():
            self.input.setText(str(value))
        else:
            if "." in old:
                decimals = old.split(".")[1]
                self.input.setText(f"{value}.{decimals}")

    def on_input_change(self):
        text = self.input.text().strip()

        if not text:
            return

        try:
            value = float(text)
        except ValueError:
            self.input.setText(str(self.slider.value()))
            return

        # ограничение диапазона
        clamped_value = max(self.min_value, min(value, self.max_value))

        # обновляем поле
        if clamped_value >= self.max_value:
            self.input.setText(str(self.max_value))
        elif clamped_value <= self.min_value:
            self.input.setText(str(self.min_value))
        else:
            # норм форматирование
            if float(clamped_value).is_integer():
                self.input.setText(str(int(clamped_value)))
            else:
                self.input.setText(f"{clamped_value:.2f}")

        # обновляем слайдер (даже если значение то же самое)
        self.slider.setValue(int(clamped_value))

# ---------------- КАСТОМНАЯ ПАНЕЛЬ ----------------  
class CastomPanel(QWidget):
    def __init__(self, radius=20,border_width=3):
        super().__init__()

        scale = get_scale(self.screen().size()) 

        self.radius = radius*scale
        self.border_width = ceil(border_width*scale)
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
        self.default_values = {
            "P_пл": 5,
            "AB": 10,
            "OA": 24,
            "OC": 8,
            "P": 10.4
        }

        scale = get_scale(self.screen().size()) 

        layout = QVBoxLayout(self)
        layout.setSpacing(ceil(5*scale))
        layout.setContentsMargins(ceil(10*scale),ceil(10*scale),ceil(10*scale),ceil(10*scale))

        self.sliders = {}
        label_dict1 = {"P_пл": "Н", "P": "Н"}
        label_dict2 = {"AB": "см", "OA": "см", "OC": "см"}

        for key in label_dict1:
            slider = Slider(label_dict1[key], key, min_value=0)  # создаём
            self.sliders[key] = slider             # сохраняем
            layout.addWidget(slider)
            layout.setSpacing(ceil(-20*scale))

        for key in label_dict2:
            slider = Slider(label_dict2[key], key, min_value=1)  # создаём
            self.sliders[key] = slider             # сохраняем
            layout.addWidget(slider)
            layout.setSpacing(ceil(-20*scale))

        layout.setSpacing(ceil(35*scale))

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
            hover_scale=1.25,
            enlarge_on_hover=True
        )
        self.reset_btn.clicked.connect(self.reset_all_sliders)

        self.random_btn = QPushButton("СЛУЧАЙНЫЕ ЗН-Я")
        self.random_btn.clicked.connect(self.random_all_sliders)
        self.random_btn.setObjectName("mainButton")
        generate_adaptive_qss(
            self.random_btn,
            base_size=(270, 47),
            base_font=15,
            base_padding=(8, 20),
            base_border_radius=14,
            base_border_width=3,
            border_color="#111111",
            hover_scale=1.25,
            enlarge_on_hover=True,
            thicker_border_on_hover=False
        )
        self.random_btn.setStyleSheet(
        self.random_btn.styleSheet() +
        "QPushButton#mainButton { background-color: #111111; color: white; }")
        btn_row.addWidget(self.reset_btn)
        btn_row.setSpacing(ceil(10*scale))
        btn_row.addWidget(self.random_btn)

        layout.addLayout(btn_row)
    
    #получить значение с слайдера
    def get_value(self, key):
        try:
            return float(self.sliders[key].input.text())
        except ValueError:
            return 0.0
    #изменить значение слайдера
        #изменить значение слайдера и текста рядом
    def set_value(self, key, value):
        if key in self.sliders:
            slider_obj = self.sliders[key]
            slider_obj.slider.setValue(int(value))
            slider_obj.input.setText(str(value))
            #self.sliders[key].slider.setValue(value)

    def reset_all_sliders(self):
        for key, value in self.default_values.items():
            self.set_value(key, value)

    def random_all_sliders(self):
        for key in self.sliders:
            self.set_value(key, randint(1, 100))

        if self.get_value('OC') > self.get_value('AB'):
            new_value = self.get_value('AB') - 1
            self.set_value('OC', max(1, new_value))

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
        self.input.setText('0') 

        # Создаем валидатор для дробных чисел
        regex = QRegularExpression(r"^-?\d+(\.\d{0,2})?$")
        validator = QRegularExpressionValidator(regex)
        self.input.setValidator(validator)

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
    def __init__(self, input_panel_ref):
        super().__init__()
        self.input_panel = input_panel_ref 

        scale = get_scale(self.screen().size()) 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(ceil(10*scale),ceil(10*scale),ceil(10*scale),ceil(10*scale))
        layout.setSpacing(ceil(10*scale))

        self.values = {}
        values_layout = QHBoxLayout()

        label_dict = {"X_0": "Н", "Y_0": "H", "Y_C": "H"}

        for key in label_dict:
            value_ans = answer_panel(label_dict[key], key)
            self.values[key] = value_ans             
            values_layout.addWidget(value_ans)
            values_layout.setSpacing(ceil(-5*scale))

        layout.addLayout(values_layout)

        # КНОПКИ
        btn_row = QHBoxLayout()

        self.reset_btn = QPushButton("СБРОСИТЬ")
        self.reset_btn.clicked.connect(self.clear_results) 
        self.reset_btn.setObjectName("secondaryButton")
        generate_adaptive_qss(
            self.reset_btn, base_size=(200, 47), base_font=15, base_padding=(8, 20),
            base_border_radius=14, base_border_width=3, border_color="#111111", hover_scale=1.25, enlarge_on_hover=True
        )
        
        self.check_btn = QPushButton("ПРОВЕРИТЬ ОТВЕТ")
        self.check_btn.clicked.connect(self.calculate_physics)  
        self.check_btn.setObjectName("mainButton")
        generate_adaptive_qss(
            self.check_btn, base_size=(270, 47), base_font=15, base_padding=(8, 20),
            base_border_radius=14, base_border_width=3, border_color="#111111", hover_scale=1.25,
            enlarge_on_hover=True, thicker_border_on_hover=False
        )
        self.check_btn.setStyleSheet(
            self.check_btn.styleSheet() +
            "QPushButton#mainButton { background-color: #111111; color: white; }"
        )
        
        btn_row.addWidget(self.reset_btn)
        btn_row.setSpacing(ceil(-5*scale))
        btn_row.addWidget(self.check_btn)
        layout.addLayout(btn_row)
        layout.addStretch()

    # --- МЕТОД СБРОСА ---
    def clear_results(self):
        self.set_value_ans("X_0", 0.0)
        self.set_value_ans("Y_0", 0.0)
        self.set_value_ans("Y_C", 0.0)

    # --- МЕТОД РАСЧЕТА ---
    def calculate_physics(self):
        try:
            weight = float(self.input_panel.get_value("P_пл")) 
            force_p = float(self.input_panel.get_value("P"))   
            side_oa = float(self.input_panel.get_value("OA"))  
            side_ab = float(self.input_panel.get_value("AB"))  
            side_oc = float(self.input_panel.get_value("OC"))  

            hypotenuse_ob = (side_oa**2 + side_ab**2) ** 0.5
            res_x0 = -force_p * (side_ab / hypotenuse_ob)
            res_yc = (2 * side_oa * weight + 3 * (hypotenuse_ob / 2) * force_p) / (3 * side_oc)
            res_y0 = force_p * (side_oa / hypotenuse_ob) + weight - res_yc

            self.set_value_ans("X_0", round(res_x0, 2))
            self.set_value_ans("Y_C", round(res_yc, 2))
            self.set_value_ans("Y_0", round(res_y0, 2))

        except Exception as e:
            show_error_message(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def get_value_ans(self, key):
        try:
            return float(self.sliders[key].input.text())
        except:
            return 0.0
        
    def set_value_ans(self, key, value):
        if key in self.values:
            self.values[key].input.setText(str(value))

# ---------------- ОСНОВНОЙ ЭКРАН ----------------
class SolverPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        scale = get_scale(self.screen().size()) 

        # Виджет для сообщения об ошибке
        self.error_label = QLabel("Некорректные значения параметров!")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setVisible(False)  # Изначально скрыт

        # Стиль для сообщения об ошибке
        error_style = f"""
        QLabel {{
            color: #111111;
            font-size: {18*scale}px;
            font-weight: bold;
            font-family: Segoe Pro;
            background-color: transparent;
        }}
        """
        self.error_label.setStyleSheet(error_style)


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
        all_layout.setContentsMargins(20*scale, 70*scale, 20*scale, 15*scale)
        all_layout.setSpacing(20*scale)

        # ---- ЛЕВАЯ ПАНЕЛЬ ----
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.input_panel = input_panel()
        self.result_panel = result_panel(self.input_panel)

        self.input_panel.set_value("OC", 8)
        self.input_panel.set_value("AB", 10)
        self.input_panel.set_value("OA", 24)
        self.input_panel.set_value("P_пл", 5)
        self.input_panel.set_value("P", 10.4)

        # Подключаем отслеживание изменений в слайдерах для проверки валидности
        for slider_key in self.input_panel.sliders:
            slider = self.input_panel.sliders[slider_key]
            slider.slider.valueChanged.connect(self.update_error_status)
            slider.input.editingFinished.connect(self.update_error_status)


        left_layout.addWidget(self.input_panel)
        left_layout.addWidget(self.result_panel)
        #left_layout.addStretch()

        #all_layout.addWidget(left_widget)

        # ---- ПРАВАЯ ПАНЕЛЬ ----
        right_widget = QWidget()
        right = QVBoxLayout(right_widget)

        self.graph = GraphWidget()
        self.graph.setMinimumHeight(250*scale)

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
            hover_scale=1.25,
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
            hover_scale=1.25,
            enlarge_on_hover=True
        )

        #self.error_label.setAlignment(Qt.AlignLeft)
        #right.addWidget(self.error_label)
        #right.setAlignment(Qt.AlignBottom)

        self.error_label.setFixedHeight(100*scale)

        btns = QVBoxLayout()
        btns.addStretch()
        btns.addWidget(self.hint)
        btns.addWidget(self.back)

        error = QVBoxLayout()
        error.addStretch()
        error.addWidget(self.error_label)

        btns.setAlignment(Qt.AlignRight)

        bttm = QHBoxLayout()
        #bttm.addSpacing(20)
        bttm.addLayout(error)
        bttm.setAlignment(Qt.AlignBottom)
        bttm.addStretch()
        bttm.addLayout(btns)

        right.addLayout(bttm)

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

    def validate_inputs(self):
        """Проверяет корректность введённых значений"""
        try:
            side_oc = float(self.input_panel.get_value("OC"))
            side_ab = float(self.input_panel.get_value("AB"))

            # Правило: OC должно быть меньше AB
            if side_oc >= side_ab:
                return False, "СТОРОНА OC ДОЛЖНА БЫТЬ МЕНЬШЕ СТОРОНЫ AB"

            return True, ""
        except Exception as e:
            return False, f"Ошибка ввода: {str(e)}"
        
    def update_error_status(self):
        """Обновляет статус ошибки — показывает/скрывает сообщение"""
        is_valid, error_message = self.validate_inputs()

        if is_valid:
            self.error_label.setVisible(False)
        else:
            self.error_label.setText(error_message)
            self.error_label.setVisible(True)

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

QPushButton#help_btn {
    font-weight: bold;               
    font-family: Gerhaus;
    color: white;
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
"""

# ---------------- ЗАПУСК ----------------
if __name__ == "__main__":
    app = QApplication([])
    
    # Загружаем шрифты
    QFontDatabase.addApplicationFont("ProjUITest/Assets/UI_FONT.otf")
    QFontDatabase.addApplicationFont("ProjUITest/Assets/TEXT_FONT.ttf")
    QFontDatabase.addApplicationFont("ProjUITest/Assets/SegoePro-Semibold.ttf")

    # Применяем стиль Fusion (обязательно для корректной работы кастомных окон)
    app.setStyle("Fusion")
    
    # Применяем наши стили
    app.setStyleSheet(STYLE)

    window = App()
    window.show()

    app.exec()