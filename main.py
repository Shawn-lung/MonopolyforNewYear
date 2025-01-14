import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QColor, QFont

# ---------------------------------------------------
# 1. 全域常數: 顏色/排序/資料結構
# ---------------------------------------------------
COLOR_MAP = {
    "綠": "#5cb85c",
    "藍": "#337ab7",
    "紅": "#d9534f",
    "黃": "#f0ad4e",
    "橘": "#f39423",
    "粉": "#f78fb3",
    "淺藍": "#87ceeb",
    "咖啡": "#8B4513",
}

COLOR_ORDER = ["咖啡", "粉", "紅", "橘", "黃", "綠", "淺藍", "藍"]


class Card:
    """ 大富翁卡片資料 """
    def __init__(
        self,
        name,
        description="",
        price="$0",
        rent="$0",
        house_rents=None,
        hotel_rent="$0",
        house_cost="$0",
        mortgage="$0",
        color="橘",
        group=None
    ):
        self.name = name
        self.description = description
        self.price = price
        self.rent = rent
        self.house_rents = house_rents if house_rents else ["$0","$0","$0","$0"]
        self.hotel_rent = hotel_rent
        self.house_cost = house_cost
        self.mortgage = mortgage
        self.color = color
        self.group = group  # "Group1" / "Group2" / "Group3" / None


# ---------------------------------------------------
# 2. 卡片「繪製」的核心函式
#    讓小卡、大卡都可共用
# ---------------------------------------------------
def render_card_image(card: Card, size: QSize) -> QPixmap:
    """
    根據卡片資料 + 指定size，回傳繪好的QPixmap(就像你給的截圖外觀)。
    包含：
      - 上方色塊 (card.color)
      - Name
      - Price、Rent
      - 虛線、房子租金、飯店、建房費、抵押金
    """
    # 建立空白 pixmap
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)

    width  = size.width()
    height = size.height()

    # 可以根據 size 大小來調整字體
    # 例如: size越大就字越大
    # 以下以比例計算做示範
    title_font_size = int(height * 0.07)   # 比如 7% 做標題
    normal_font_size= int(height * 0.05)
    small_font_size = int(height * 0.04)

    titleFont = QFont("Arial", title_font_size, QFont.Bold)
    normalFont= QFont("Arial", normal_font_size)
    smallFont = QFont("Arial", small_font_size)

    # 1) 上方色塊
    bg_color = COLOR_MAP.get(card.color, "#f39423")
    p.setBrush(QColor(bg_color))
    p.setPen(Qt.NoPen)
    # 預留上方 ~15% 高度做色塊
    header_h = int(height * 0.18)
    p.drawRect(0, 0, width, header_h)

    # 2) 卡片標題(名稱)
    p.setPen(Qt.black)
    p.setFont(titleFont)
    text_rect = (0, 0, width, header_h)
    p.drawText(*text_rect, Qt.AlignCenter, card.name)

    # 3) 白底區域
    p.setBrush(Qt.white)
    p.setPen(Qt.NoPen)
    p.drawRect(0, header_h, width, height - header_h)

    p.setPen(Qt.black)

    # 從 header_h+一些padding 開始印文字
    current_y = header_h + int(height * 0.05)

    # 4) Price / Rent
    p.setFont(normalFont)
    line_height = int(height * 0.06)
    p.drawText(5, current_y, f"Price {card.price}")
    current_y += line_height
    p.drawText(5, current_y, f"Rent {card.rent}")
    current_y += line_height

    # 5) 虛線
    p.drawText(5, current_y, "----------------------------")
    current_y += line_height

    # 6) 房子租金 (With 1~4 House, With 1 Hotel)
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

    # 7) 虛線
    p.drawText(5, current_y, "----------------------------")
    current_y += line_height

    # 8) 一棟房價格, 抵押
    p.setFont(smallFont)
    p.drawText(5, current_y, f"One house cost {card.house_cost}")
    current_y += line_height
    p.drawText(5, current_y, f"Mortgage {card.mortgage}")

    p.end()
    return pixmap


# ---------------------------------------------------
# 3. 小卡 (CardWidget)
#    直接利用 render_card_image(...) 產生 160x220 的卡面
# ---------------------------------------------------
class CardWidget(QLabel):
    def __init__(self, card: Card, parent=None):
        super().__init__(parent)
        self.card = card
        self.setAcceptDrops(False)

        self.drag_start_pos = QPoint()
        self.normal_size = QSize(160, 220)  # 小卡大小

        self.updateCardAppearance()

    def updateCardAppearance(self):
        """ 重新繪製小卡外觀 """
        pixmap = render_card_image(self.card, self.normal_size)
        self.setPixmap(pixmap)
        self.setFixedSize(self.normal_size)

    # ------------ 滑鼠事件: 拖曳 & 雙擊 ------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.showLargeCard()
        super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            distance = (event.pos() - self.drag_start_pos).manhattanLength()
            if distance > 5:
                self.startDrag()
        super().mouseMoveEvent(event)

    def startDrag(self):
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.card.name)
        drag.setMimeData(mime_data)

        # 拖曳時的縮圖
        drag_pixmap = self.pixmap().copy()  # 直接用目前顯示的pixmap即可
        drag.setPixmap(drag_pixmap)

        drop_action = drag.exec_(Qt.MoveAction)

    def showLargeCard(self):
        """ 打開放大的對話框顯示同一張卡面 (例如 400x550) """
        dialog = ZoomCardDialog(self.card, parent=self)
        dialog.exec_()


# ---------------------------------------------------
# 4. 放大卡片的 Dialog
# ---------------------------------------------------
class ZoomCardDialog(QDialog):
    def __init__(self, card: Card, parent=None):
        super().__init__(parent)
        self.card = card
        self.setWindowTitle("放大卡片 - " + self.card.name)

        # 設定對話框大小
        self.resize(500, 700)

        # 建立顯示卡片的Label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        # 佈局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 繪製放大卡面
        self.updateLargeCard()

    def updateLargeCard(self):
        """ 使用 render_card_image() 產生更大尺寸的卡面 """
        large_size = QSize(400, 550)  # 你要多大都可以
        pixmap = render_card_image(self.card, large_size)
        self.label.setPixmap(pixmap)


# ---------------------------------------------------
# 5. 可放置卡片的區域
# ---------------------------------------------------
class AreaWidget(QFrame):
    def __init__(self, area_name, parent=None):
        super().__init__(parent)
        self.area_name = area_name
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet("background-color: #EAEAEA;")

        # 若不是Center, 放一個照片框
        if self.area_name != "Center":
            self.photoFrame = QFrame(self)
            self.photoFrame.setStyleSheet("background-color: #CCCCCC;")
            self.photoFrame.setFixedSize(80, 80)
            self.layout.addWidget(self.photoFrame)

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

            # 從舊容器移除
            old_parent = source_widget.parent()
            if isinstance(old_parent, AreaWidget):
                old_parent.layout.removeWidget(source_widget)

            # 加到新容器
            self.layout.addWidget(source_widget)
            self.sortByColor()
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def sortByColor(self):
        start_index = 1 if (self.area_name != "Center") else 0
        widgets = []
        for i in range(start_index, self.layout.count()):
            w = self.layout.itemAt(i).widget()
            widgets.append(w)

        def color_key(w):
            c = w.card.color
            try:
                return COLOR_ORDER.index(c)
            except ValueError:
                return len(COLOR_ORDER)

        widgets.sort(key=color_key)

        # 先清除再加回
        for i in range(start_index, self.layout.count()):
            item = self.layout.itemAt(start_index)
            if item:
                self.layout.removeItem(item)

        for w in widgets:
            self.layout.addWidget(w)


# ---------------------------------------------------
# 6. 主視窗
# ---------------------------------------------------
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 全螢幕
        self.showFullScreen()
        self.setWindowTitle("大富翁卡片 - 小卡/放大卡")

        # 主容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # 左：三個 Group
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

        # 右：Center
        self.center_area = AreaWidget("Center")

        main_layout.addWidget(left_container, stretch=1)
        main_layout.addWidget(self.center_area, stretch=1)

        # 建立卡片
        self.cards = [
            Card(name="New York Ave", color="橘", price="$210", rent="$14",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",
                 description="地價210,過路費14"),
            Card(name="台北車站", color="紅", price="$300", rent="$30",
                 house_rents=["$60","$90","$120","$150"], hotel_rent="$200",
                 description="台北最重要車站"),
            Card(name="機場", color="藍", price="$2000", rent="$200",
                 house_rents=["$400","$600","$800","$1000"], hotel_rent="$1200",
                 description="出國旅行從此出發"),
            Card(name="西門町", color="粉", price="$500", rent="$50",
                 house_rents=["$100","$200","$300","$400"], hotel_rent="$600",
                 description="台北商圈熱鬧地段"),
            Card(name="101 大樓", color="綠", price="$1500", rent="$150",
                 house_rents=["$300","$450","$600","$750"], hotel_rent="$900",
                 description="台北地標"),
            Card(name="102 大樓", color="綠", price="$1500", rent="$150",
                 house_rents=["$300","$450","$600","$750"], hotel_rent="$900",
                 description="台北地標"),
            Card(name="103 大樓", color="綠", price="$1500", rent="$150",
                 house_rents=["$300","$450","$600","$750"], hotel_rent="$900",
                 description="台北地標"),
            Card(name="104 大樓", color="綠", price="$1500", rent="$150",
                 house_rents=["$300","$450","$600","$750"], hotel_rent="$900",
                 description="台北地標"),
        ]

        # 建立 CardWidget 放到 Center
        for c in self.cards:
            w = CardWidget(c)
            self.center_area.layout.addWidget(w)
        self.center_area.sortByColor()


# ---------------------------------------------------
# 7. 程式進入點
# ---------------------------------------------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # 其實已在建構子呼叫 showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
