# dialogs.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont

from widgets import render_card_image, CardWidget
from models import Card

class ZoomCardDialog(QDialog):
    """
    放大顯示卡片的對話框。
    """
    def __init__(self, card_widget: CardWidget, card: Card, parent=None):
        super().__init__(parent)
        self.card_widget = card_widget
        self.card = card

        self.setWindowTitle("放大卡片 - " + self.card.name)
        self.resize(500, 700)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # 若是「監獄卡」，就加「使用」按鈕
        if self.card.name == "監獄卡":
            self.use_button = QPushButton("使用監獄卡")
            layout.addWidget(self.use_button)
            self.use_button.clicked.connect(self.on_use_jail_card)
        else:
            # 抵押/解除抵押按鈕
            self.mortgage_button = QPushButton("抵押" if not self.card.is_mortgaged else "解除抵押")
            layout.addWidget(self.mortgage_button)
            self.mortgage_button.clicked.connect(self.on_toggle_mortgage)

        # 關閉按鈕
        self.close_button = QPushButton("關閉")
        layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

        self.setLayout(layout)
        self.updateLargeCard()

    def updateLargeCard(self):
        large_size = QSize(400, 550)
        pixmap = render_card_image(self.card, large_size, self.card.is_mortgaged)
        self.label.setPixmap(pixmap)

    def on_use_jail_card(self):
        """
        使用監獄卡的動作 (可自行擴充遊戲邏輯)。
        目前只是把卡片從畫面拿掉。
        """
        self.card_widget.setParent(None)
        self.close()

    def on_toggle_mortgage(self):
        """
        抵押/解除抵押
        """
        self.card_widget.toggle_mortgage()
        self.updateLargeCard()
        self.mortgage_button.setText("抵押" if not self.card.is_mortgaged else "解除抵押")


class RiddleDialog(QDialog):
    """
    謎題對話框。
    """
    def __init__(self, question: str, answer: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("謎題")

        big_font = QFont("微軟正黑體", 24, QFont.Bold)

        self.question_label = QLabel(question, self)
        self.question_label.setFont(big_font)

        self.answer_button = QPushButton("顯示答案", self)
        self.answer_button.setFont(QFont("微軟正黑體", 18))

        self.answer_label = QLabel("", self)
        self.answer_label.setFont(QFont("微軟正黑體", 24))

        self.close_button = QPushButton("關閉謎題", self)
        self.close_button.setFont(QFont("微軟正黑體", 18))

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        layout.addWidget(self.answer_button)
        layout.addWidget(self.answer_label)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        self.answer_button.clicked.connect(lambda: self.show_answer(answer))
        self.close_button.clicked.connect(self.close)

    def show_answer(self, answer_text: str):
        self.answer_label.setText(answer_text)
