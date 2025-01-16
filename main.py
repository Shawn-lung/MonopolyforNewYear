# main.py
import sys, random
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QScrollArea, 
    QFrame, QLabel, QDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QFont, QColor

from flowlayout import FlowLayout  
from data_source import WELFARE_CARDS, CHANCE_CARDS, RIDDLES
# -----------------------------------------
# 顏色、排序、卡片資料
# -----------------------------------------
COLOR_MAP = {
    "綠": "#5cb85c",
    "藍": "#337ab7",
    "紅": "#d9534f",
    "黃": "#ffde59",
    "橘": "#f39423",
    "粉": "#f78fb3",
    "淺藍": "#87ceeb",
    "咖啡": "#8B4513",
    "交通": "#d9d9d9",
    "公司": "#d9d9d9"
}

COLOR_ORDER = ["咖啡", "淺藍", "粉", "橘", "紅", "黃", "綠", "藍", "交通", "公司"]


class Card:
    def __init__(
        self,
        name,
        description="",
        price="$0",
        rent="$0",
        set_rent =  "$0",
        house_rents=None,
        hotel_rent="$0",
        house_cost="$0",
        mortgage="$0",
        unmortgage="$0",
        color="橘",
        group=None
    ):
        self.name = name
        self.description = description
        self.price = price
        self.rent = rent
        self.set_rent = set_rent
        self.house_rents = house_rents if house_rents else ["$0","$0","$0","$0"]
        self.hotel_rent = hotel_rent
        self.house_cost = house_cost
        self.mortgage = mortgage
        self.unmortgage = unmortgage
        self.color = color
        self.group = group

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def render_card_image(card: Card, size: QSize) -> QPixmap:
    """
    繪製不同卡片版型(一般/交通/公司)。
    """
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)

    width  = size.width()
    height = size.height()

    title_font_size = int(height * 0.07)
    normal_font_size= int(height * 0.05)
    small_font_size = int(height * 0.04)

    titleFont = QFont("Arial", title_font_size, QFont.Bold)
    normalFont= QFont("Arial", normal_font_size)
    smallFont = QFont("Arial", small_font_size)

    header_h = int(height * 0.18)

    bg_color = COLOR_MAP.get(card.color, "#f39423")
    # 上方色塊
    p.setBrush(QColor(bg_color))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 0, width, header_h)

    # 卡片標題
    p.setPen(Qt.black)
    p.setFont(titleFont)
    p.drawText(0, 0, width, header_h, Qt.AlignCenter, card.name)

    # 下方白底
    p.setBrush(Qt.white)
    p.setPen(Qt.NoPen)
    p.drawRect(0, header_h, width, height - header_h)

    p.setPen(Qt.black)

    if card.color == "交通":
        p.setFont(normalFont)
        current_y = header_h + int(height * 0.10)
        line_height = int(height * 0.06)
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        lines = [
            f"1 transportation: $25",
            f"2 transportations: $50",
            f"3 transportations: $100",
            f"4 transportations: $200",
        ]
        for text_line in lines:
            p.drawText(5, current_y, text_line)
            current_y += line_height
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        p.setFont(smallFont)
        p.drawText(5, current_y, f"Mortgage $100")
        current_y += line_height
        p.drawText(5, current_y, f"Unmortgage $110")

    elif card.color == "公司":
        p.setFont(normalFont)
        current_y = header_h + int(height * 0.10)
        line_height = int(height * 0.06)
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        lines = [
            "1 corporation : dice×4",
            "2 corporations: dice×10",
            "3 corporations: dice×30",
        ]
        for text_line in lines:
            p.drawText(5, current_y, text_line)
            current_y += line_height
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        p.setFont(smallFont)
        p.drawText(5, current_y, f"Mortgage $75")
        current_y += line_height
        p.drawText(5, current_y, f"Unmortgage $83")
    elif card.name == "監獄卡":
        p.setFont(normalFont)
        current_y = header_h + int(height * 0.10)
        line_height = int(height * 0.06)
        p.drawText(5, current_y, "你可以使用此卡出獄")
        current_y += line_height
        
    else:
        # 一般地產
        p.setFont(normalFont)
        current_y = header_h + int(height * 0.05)
        line_height = int(height * 0.06)

        p.drawText(5, current_y, f"Price {card.price}")
        current_y += line_height
        p.drawText(5, current_y, f"Rent {card.rent}")
        current_y += line_height
        p.drawText(5, current_y, f"Rent w/ set {card.set_rent}")
        current_y += line_height
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height

        houseLabels = [
            f"With 1 house  {card.house_rents[0]}",
            f"With 2 house  {card.house_rents[1]}",
            f"With 3 house  {card.house_rents[2]}",
            f"With 4 house  {card.house_rents[3]}",
            f"With 1 Hotel  {card.hotel_rent}",
        ]
        for label in houseLabels:
            p.drawText(5, current_y, label)
            current_y += line_height

        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        p.setFont(smallFont)
        p.drawText(5, current_y, f"One house cost {card.house_cost}")
        current_y += line_height
        p.drawText(5, current_y, f"Mortgage {card.mortgage}")
        current_y += line_height
        p.drawText(5, current_y, f"Unmortgage {card.unmortgage}")

    p.end()
    return pixmap


class CardWidget(QLabel):
    """卡片縮圖 + 拖曳 + 雙擊放大"""
    def __init__(self, card: Card, parent=None):
        super().__init__(parent)
        self.card = card
        self.drag_start_pos = QPoint()
        self.normal_size = QSize(160, 220)
        self.updateCardAppearance()

    def updateCardAppearance(self):
        pixmap = render_card_image(self.card, self.normal_size)
        self.setPixmap(pixmap)
        self.setFixedSize(self.normal_size)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            distance = (event.pos() - self.drag_start_pos).manhattanLength()
            if distance > 5:
                self.startDrag()
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.showLargeCard()
        super().mouseDoubleClickEvent(event)

    def startDrag(self):
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.card.name)
        drag.setMimeData(mime_data)

        drag_pixmap = self.pixmap().copy()
        drag.setPixmap(drag_pixmap)
        drop_action = drag.exec_(Qt.MoveAction)

    def showLargeCard(self):
        def use_card_callback(card_w):
            """
            這個函式會被 ZoomCardDialog 呼叫,
            負責真正移除卡片
            """
            # 取得卡片當前的父容器 (可能是 AreaWidget)
            parent_w = card_w.parent()
            if parent_w and hasattr(parent_w, 'flowLayout'):
                parent_w.flowLayout.removeWidget(card_w)
            card_w.setParent(None)

        dialog = ZoomCardDialog(card_widget=self, card=self.card, on_use_card=use_card_callback, parent=self)
        dialog.exec_()



class ZoomCardDialog(QDialog):
    def __init__(self, card_widget, card, on_use_card=None, parent=None):
        super().__init__(parent)
        self.card_widget = card_widget
        self.card = card
        self.on_use_card = on_use_card  # 這就是外部傳來的 callback

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

        # 關閉按鈕
        self.close_button = QPushButton("關閉")
        layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

        self.setLayout(layout)
        self.updateLargeCard()

    def updateLargeCard(self):
        large_size = QSize(400, 550)
        pixmap = render_card_image(self.card, large_size)
        self.label.setPixmap(pixmap)

    def on_use_jail_card(self):
        """
        按下「使用監獄卡」
        """
        if self.on_use_card is not None:
            self.on_use_card(self.card_widget)  # 呼叫外部傳進來的 callback
        self.close()



class AreaWidget(QScrollArea):
    """
    一個區域 (Group1/2/3 或 Center)，可放多張卡片 (CardWidget)。
    使用 FlowLayout 來自動換行。
    """
    def __init__(self, area_name, parent=None):
        super().__init__(parent)
        self.area_name = area_name
        self.setAcceptDrops(True)

        self.container = QWidget()
        self.flowLayout = FlowLayout(self.container, margin=10, spacing=10)
        self.container.setLayout(self.flowLayout)

        # 如果不是Center，就插入圖片(組員照片)示範
        if self.area_name != "Center":
            photoFrame = QLabel(self.container)
            photoFrame.setStyleSheet("border:1px solid #999;")
            photoFrame.setFixedSize(80, 80)
            image_path = resource_path(area_name + ".png") 

            pixmap = QPixmap(image_path)  # 如 "Group1.png", "Group2.png"...
            scaled_pix = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            photoFrame.setPixmap(scaled_pix)
            photoFrame.setAlignment(Qt.AlignCenter)

            self.flowLayout.addWidget(photoFrame)

        self.setWidget(self.container)
        self.setWidgetResizable(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        source_widget = event.source()
        if isinstance(source_widget, CardWidget):
            # 更新 group
            if self.area_name == "Center":
                source_widget.card.group = None
            else:
                source_widget.card.group = self.area_name

            # 從舊容器拿走
            old_parent = source_widget.parent()
            if isinstance(old_parent, AreaWidget):
                old_parent.flowLayout.removeWidget(source_widget)

            # 放到本區
            self.flowLayout.addWidget(source_widget)

            # 排序
            self.sortByColor()

            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def sortByColor(self):
        tempList = []
        for i in range(self.flowLayout.count()):
            item = self.flowLayout.itemAt(i)
            w = item.widget()
            tempList.append(w)

        photoFrame = None
        if self.area_name != "Center" and len(tempList) > 0:
            photoFrame = tempList[0]
            cardWidgets = tempList[1:]
        else:
            cardWidgets = tempList

        def color_key(w):
            c = w.card.color
            try:
                return COLOR_ORDER.index(c)
            except ValueError:
                return len(COLOR_ORDER)

        cardWidgets = [w for w in cardWidgets if isinstance(w, CardWidget)]
        cardWidgets.sort(key=color_key)

        for i in range(self.flowLayout.count()):
            self.flowLayout.takeAt(0)

        if photoFrame:
            self.flowLayout.addWidget(photoFrame)

        for w in cardWidgets:
            self.flowLayout.addWidget(w)


# ---------------------------------------------------------
# 新增的：福利卡、機會卡、謎題
# ---------------------------------------------------------
class RiddleDialog(QDialog):
    def __init__(self, question, answer, parent=None):
        super().__init__(parent)
        self.setWindowTitle("謎題")

        # 可以設定一個大字體
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

    def show_answer(self, answer_text):
        self.answer_label.setText(answer_text)


# -----------------------------------------
# 主視窗
# -----------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.setWindowTitle("大富翁卡片 (FlowLayout + ScrollArea) - 含抽卡 & 謎題")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 上方按鈕區 (抽福利卡、抽機會卡、抽謎題)
        self.original_welfare_cards = list(WELFARE_CARDS)
        self.original_chance_cards  = list(CHANCE_CARDS)
        self.original_riddles       = list(RIDDLES)

        # 建立「目前可抽」庫
        self.welfare_cards = list(self.original_welfare_cards)
        self.chance_cards  = list(self.original_chance_cards)
        self.riddles       = list(self.original_riddles)

        button_layout = QHBoxLayout()
        self.btn_welfare = QPushButton("抽福利卡")
        self.btn_chance = QPushButton("抽機會卡")
        self.btn_riddle = QPushButton("抽謎題")

        button_layout.addWidget(self.btn_welfare)
        button_layout.addWidget(self.btn_chance)
        button_layout.addWidget(self.btn_riddle)

        self.btn_welfare.clicked.connect(self.draw_welfare_card)
        self.btn_chance.clicked.connect(self.draw_chance_card)
        self.btn_riddle.clicked.connect(self.draw_riddle)

        main_layout.addLayout(button_layout)

        # 下方放 左邊的 Groups + 右邊的 Center
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout, stretch=1)

        left_container = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        left_container.setLayout(left_layout)

        self.group1_area = AreaWidget("Group1")
        self.group2_area = AreaWidget("Group2")
        self.group3_area = AreaWidget("Group3")

        left_layout.addWidget(self.group1_area)
        left_layout.addWidget(self.group2_area)
        left_layout.addWidget(self.group3_area)

        self.center_area = AreaWidget("Center")

        content_layout.addWidget(left_container, stretch=1)
        content_layout.addWidget(self.center_area, stretch=2)

        # --- 大富翁主要卡片 (示範) ---
        self.cards = [
            Card(name="小港", color="咖啡", price="$60", rent="$2", set_rent="$4",
                 house_rents=["$10","$30","$90","$160"], hotel_rent="$250",house_cost="$50",mortgage="$30",unmortgage = "$33"),
            Card(name="大寮", color="咖啡", price="$60", rent="$4", set_rent="$8",
                 house_rents=["$20","$60","$180","$320"], hotel_rent="$450",house_cost="$50",mortgage="$30",unmortgage = "$33"),
            Card(name="左營高鐵站", color="交通", price="$200"),
            Card(name="清水", color="淺藍", price="$100", rent="$6", set_rent="$12",
                 house_rents=["$30","$90","$270","$400"], hotel_rent="$550",house_cost="$50",mortgage="$50",unmortgage = "$55"),
            Card(name="台中遠雄", color="淺藍", price="$100", rent="$6", set_rent="$12",
                 house_rents=["$30","$90","$270","$400"], hotel_rent="$550",house_cost="$50",mortgage="$50",unmortgage = "$55"),
            Card(name="烏日", color="淺藍", price="$120", rent="$8", set_rent="$16",
                 house_rents=["$40","$100","$300","$450"], hotel_rent="$600",house_cost="$50",mortgage="$60",unmortgage = "$66"),
            Card(name="夢時代", color="粉", price="$140", rent="$10", set_rent="$20", 
                 house_rents=["$50","$150","$450","$625"], hotel_rent="$750",house_cost="$100",mortgage="$70",unmortgage = "$77"),
            Card(name="純文實業", color="公司", price="$150"),
            Card(name="鳳山", color="粉", price="$140", rent="$10", set_rent="$20", 
                 house_rents=["$50","$150","$450","$625"], hotel_rent="$750",house_cost="$100",mortgage="$70",unmortgage = "$77"),
            Card(name="海港", color="粉", price="$160", rent="$12", set_rent="$24",
                 house_rents=["$60","$180","$500","$700"], hotel_rent="$900",house_cost="$100",mortgage="$80",unmortgage = "$88"),
            Card(name="桃園機場", color="交通", price="$200"),
            Card(name="中央大學", color="橘", price="$180", rent="$14", set_rent="$28",
                 house_rents=["$70","$200","$550","$750"], hotel_rent="$950",house_cost="$100",mortgage="$90",unmortgage = "$99"),
            Card(name="白帥帥新光店", color="橘", price="$180", rent="$14", set_rent="$28",
                 house_rents=["$70","$200","$550","$750"], hotel_rent="$950",house_cost="$100",mortgage="$90",unmortgage = "$99"),
            Card(name="義大飯店", color="橘", price="$200", rent="$16", set_rent="$32",
                 house_rents=["$80","$220","$600","$800"], hotel_rent="$1000",house_cost="$100",mortgage="$100",unmortgage = "$110"),
            Card(name="白帥帥興中店", color="紅", price="$220", rent="$18", set_rent="$36",
                 house_rents=["$90","$250","$700","$875"], hotel_rent="$1050",house_cost="$150",mortgage="$110",unmortgage = "$121"),
            Card(name="台灣大學", color="紅", price="$220", rent="$18", set_rent="$36",
                 house_rents=["$90","$250","$700","$875"], hotel_rent="$1050",house_cost="$150",mortgage="$110",unmortgage = "$121"),
            Card(name="北師大", color="紅", price="$240", rent="$20", set_rent="$40",
                 house_rents=["$100","$300","$750","$925"], hotel_rent="$1100",house_cost="$150",mortgage="$120",unmortgage = "$132"),
            Card(name="台北高鐵站", color="交通", price="$200"),
            Card(name="海洋大學", color="黃", price="$260", rent="$22", set_rent="$44",
                 house_rents=["$110","$330","$800","$975"], hotel_rent="$1150",house_cost="$150",mortgage="$130",unmortgage = "$143"),
            Card(name="薇閣中學", color="黃", price="$260", rent="$22", set_rent="$44",
                 house_rents=["$110","$330","$800","$975"], hotel_rent="$1150",house_cost="$150",mortgage="$130",unmortgage = "$143"),
            Card(name="洪志淳皮膚科", color="公司", price="$150"),
            Card(name="天母", color="黃", price="$280", rent="$24", set_rent="$48",
                 house_rents=["$120","$360","$850","$1025"], hotel_rent="$1200",house_cost="$150",mortgage="$140",unmortgage = "$154"),
            Card(name="昭明國小", color="綠", price="$300", rent="$26", set_rent="$52",
                 house_rents=["$130","$390","$900","$1100"], hotel_rent="$1275",house_cost="$200",mortgage="$150",unmortgage = "$165"),
            Card(name="信義國小", color="綠", price="$300", rent="$26", set_rent="$52",
                 house_rents=["$130","$390","$900","$1100"], hotel_rent="$1275",house_cost="$200",mortgage="$150",unmortgage = "$165"),
            Card(name="蒲園", color="綠", price="$320", rent="$28", set_rent="$56",
                 house_rents=["$150","$450","$1000","$1200"], hotel_rent="$1400",house_cost="$200",mortgage="$160",unmortgage = "$176"),
            Card(name="阿姆斯特丹機場", color="交通", price="$200"),
            Card(name="SMG", color="藍", price="$350", rent="$35", set_rent="$70",
                 house_rents=["$175","$500","$1100","$1300"], hotel_rent="$1500",house_cost="$200",mortgage="$175",unmortgage = "$193"),
            Card(name="KaaK Group", color="公司", price="$150"),     
            Card(name="倫敦", color="藍", price="$400", rent="$50", set_rent="$100",
                 house_rents=["$200","$600","$1400","$1700"], hotel_rent="$2000",house_cost="$200",mortgage="$200",unmortgage = "$220"),
        ]
        for c in self.cards:
            w = CardWidget(c)
            self.center_area.flowLayout.addWidget(w)
        self.center_area.sortByColor()

        # -----------------------------------------------------
        # 以下為：福利卡庫、機會卡庫、謎題庫
        # -----------------------------------------------------

    # ------------------ 福利卡功能 ------------------
    def draw_welfare_card(self):
        if not self.welfare_cards:
            self.welfare_cards = list(self.original_welfare_cards)

        chosen = random.choice(self.welfare_cards)
        self.welfare_cards.remove(chosen)

        name = chosen["name"]
        desc = chosen["desc"]

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("福利卡")

        # 在文字前面也可加大標題
        big_text = f"<h2>你抽到了：</h2><p><b>{name}</b><br>{desc}</p>"
        msg_box.setText(big_text)

        # 設置字體
        big_font = QFont("微軟正黑體", 20)
        msg_box.setFont(big_font)

        msg_box.exec_()

        if name == "監獄卡":
            # 產生一張「監獄卡」CardWidget，讓玩家可以拖到某組
            jail_card = Card(name="監獄卡", color="粉", price="", rent="", set_rent="", 
                             house_rents=["","","",""], hotel_rent="", house_cost="", mortgage="",unmortgage="")
            w = CardWidget(jail_card)
            self.center_area.flowLayout.addWidget(w)
            self.center_area.sortByColor()

    # ------------------ 機會卡功能 ------------------
    def draw_chance_card(self):
        """
        隨機抽一張機會卡 -> 移除 -> 顯示
        若機會卡抽完，也重置
        """
        if not self.chance_cards:
            self.chance_cards = list(self.original_chance_cards)
        chosen = random.choice(self.chance_cards)
        self.chance_cards.remove(chosen)

        name = chosen["name"]
        desc = chosen["desc"]
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("福利卡")

        # 在文字前面也可加大標題
        big_text = f"<h2>你抽到了：</h2><p><b>{name}</b><br>{desc}</p>"
        msg_box.setText(big_text)

        # 設置字體
        big_font = QFont("微軟正黑體", 20)
        msg_box.setFont(big_font)

        msg_box.exec_()

        if name == "監獄卡":
            # 產生一張「監獄卡」CardWidget，讓玩家可以拖到某組
            jail_card = Card(name="監獄卡", color="粉", price="", rent="", set_rent="", 
                             house_rents=["","","",""], hotel_rent="", house_cost="", mortgage="",unmortgage="")
            w = CardWidget(jail_card)
            self.center_area.flowLayout.addWidget(w)
            self.center_area.sortByColor()
        # 根據卡片內容做相應動作(本範例僅顯示訊息，你可自行擴充)

    # ------------------ 謎題功能 ------------------
    def draw_riddle(self):
        """
        隨機抽一個謎題 -> 移除 -> 用RiddleDialog顯示
        若題庫清空，也重置
        """
        if not self.riddles:
            self.riddles = list(self.original_riddles)

        chosen = random.choice(self.riddles)
        self.riddles.remove(chosen)

        question = chosen["question"]
        answer = chosen["answer"]

        dlg = RiddleDialog(question, answer, self)
        dlg.exec_()


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
