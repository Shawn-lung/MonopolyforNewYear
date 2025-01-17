# main_window.py

import random
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox
)
from data_source import WELFARE_CARDS, CHANCE_CARDS, RIDDLES
from widgets import AreaWidget, CardWidget
from dialogs import RiddleDialog
from models import Card
from cards_data import cards_info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.setWindowTitle("大富翁卡片 (FlowLayout + ScrollArea) - 含抽卡 & 謎題")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 上方按鈕區 (抽福利卡、抽機會卡、抽謎題)
        self.original_welfare_cards = list(WELFARE_CARDS)
        self.original_chance_cards  = list(CHANCE_CARDS)
        self.original_riddles       = list(RIDDLES)

        self.welfare_cards = list(self.original_welfare_cards)
        self.chance_cards  = list(self.original_chance_cards)
        self.riddles       = list(self.original_riddles)

        button_layout = QHBoxLayout()
        self.btn_welfare = QPushButton("抽福利卡")
        self.btn_chance = QPushButton("抽機會卡")
        self.btn_riddle = QPushButton("抽謎題")

        self.btn_welfare.clicked.connect(self.draw_welfare_card)
        self.btn_chance.clicked.connect(self.draw_chance_card)
        self.btn_riddle.clicked.connect(self.draw_riddle)

        button_layout.addWidget(self.btn_welfare)
        button_layout.addWidget(self.btn_chance)
        button_layout.addWidget(self.btn_riddle)
        main_layout.addLayout(button_layout)

        # 下方：左(三個Group) + 右(Center)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout, stretch=1)

        # 左邊三個區塊
        self.group1_area = AreaWidget("Group1")
        self.group2_area = AreaWidget("Group2")
        self.group3_area = AreaWidget("Group3")

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(10)
        left_layout.addWidget(self.group1_area)
        left_layout.addWidget(self.group2_area)
        left_layout.addWidget(self.group3_area)

        # 右邊中心區
        self.center_area = AreaWidget("Center")

        content_layout.addWidget(left_container, stretch=1)
        content_layout.addWidget(self.center_area, stretch=2)

        # 放一些示範卡片到 Center
        self.cards = []
        for card_dict in cards_info:
            # 用 dict 解包的方式給到 Card
            new_card = Card(
                name=card_dict["name"],
                color=card_dict.get("color", "咖啡"),
                price=card_dict.get("price", "$0"),
                rent=card_dict.get("rent", "$0"),
                set_rent=card_dict.get("set_rent", "$0"),
                house_rents=card_dict.get("house_rents", ["$0","$0","$0","$0"]),
                hotel_rent=card_dict.get("hotel_rent", "$0"),
                house_cost=card_dict.get("house_cost", "$0"),
                mortgage=card_dict.get("mortgage", "$0"),
                unmortgage=card_dict.get("unmortgage", "$0"),
            )
            self.cards.append(new_card)

        for c in self.cards:
            w = CardWidget(c)
            self.center_area.flowLayout.addWidget(w)
        self.center_area.sortByColor()

    def draw_welfare_card(self):
        """
        隨機抽一張福利卡 -> 從庫中移除 -> 顯示
        若福利卡抽完，也重置。
        """
        if not self.welfare_cards:
            self.welfare_cards = list(self.original_welfare_cards)

        chosen = random.choice(self.welfare_cards)
        self.welfare_cards.remove(chosen)

        name = chosen["name"]
        desc = chosen["desc"]

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("福利卡")
        big_text = f"<h2>你抽到了：</h2><p><b>{name}</b><br>{desc}</p>"
        msg_box.setText(big_text)
        msg_box.exec_()

        if name == "監獄卡":
            # 新增一張監獄卡到場上
            jail_card = Card(name="監獄卡", color="粉")
            w = CardWidget(jail_card)
            self.center_area.flowLayout.addWidget(w)
            self.center_area.sortByColor()

    def draw_chance_card(self):
        """
        隨機抽一張機會卡 -> 移除 -> 顯示
        若機會卡抽完，也重置。
        """
        if not self.chance_cards:
            self.chance_cards = list(self.original_chance_cards)

        chosen = random.choice(self.chance_cards)
        self.chance_cards.remove(chosen)

        name = chosen["name"]
        desc = chosen["desc"]

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("機會卡")
        big_text = f"<h2>你抽到了：</h2><p><b>{name}</b><br>{desc}</p>"
        msg_box.setText(big_text)
        msg_box.exec_()

        if "監獄卡" in name:
            # 新增一張監獄卡
            jail_card = Card(name="監獄卡", color="粉")
            w = CardWidget(jail_card)
            self.center_area.flowLayout.addWidget(w)
            self.center_area.sortByColor()

    def draw_riddle(self):
        """
        隨機抽一個謎題 -> 顯示對話框
        若題庫清空，也重置。
        """
        if not self.riddles:
            self.riddles = list(self.original_riddles)

        chosen = random.choice(self.riddles)
        self.riddles.remove(chosen)

        question = chosen["question"]
        answer = chosen["answer"]

        dlg = RiddleDialog(question, answer, self)
        dlg.exec_()
