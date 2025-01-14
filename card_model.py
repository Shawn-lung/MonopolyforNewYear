import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QScrollArea, QMessageBox,
    QFrame, QLabel, QDialog, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QFont, QColor

# 1) 先把我們的 FlowLayout 類別貼在這 (或另檔import)
from flowlayout import FlowLayout  # 若放同檔，可直接使用

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
        self.group = group


# -----------------------------------------
# 繪製卡片(小/大)的函式 (略同前例)
# -----------------------------------------
def render_card_image(card: Card, size: QSize) -> QPixmap:
    """
    根據 card.color 判斷要繪製「一般房地產卡面」或
    「交通卡面」或「公司卡面」。
    """
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)

    width  = size.width()
    height = size.height()

    # 字體大小: 可依卡片大小做比例
    title_font_size = int(height * 0.07)
    normal_font_size= int(height * 0.05)
    small_font_size = int(height * 0.04)

    titleFont = QFont("Arial", title_font_size, QFont.Bold)
    normalFont= QFont("Arial", normal_font_size)
    smallFont = QFont("Arial", small_font_size)

    # 上方色塊高度
    header_h = int(height * 0.18)

    # 取得對應顏色 (預設橘)
    bg_color = COLOR_MAP.get(card.color, "#f39423")

    # -- 畫上方色塊 --
    p.setBrush(QColor(bg_color))
    p.setPen(Qt.NoPen)
    p.drawRect(0, 0, width, header_h)

    # -- 卡片標題(名稱) --
    p.setPen(Qt.black)
    p.setFont(titleFont)
    p.drawText(0, 0, width, header_h, Qt.AlignCenter, card.name)

    # -- 下方白底 --
    p.setBrush(Qt.white)
    p.setPen(Qt.NoPen)
    p.drawRect(0, header_h, width, height - header_h)

    p.setPen(Qt.black)
    # 接下來要根據color, 顯示不同版型
    if card.color == "交通":
        # 交通卡面
        # 例：with 1 transportation: 20, 2 transportations: 50, 3 transportations: 100, 4 transportations: 200
        p.setFont(normalFont)
        current_y = header_h + int(height * 0.10)
        line_height = int(height * 0.06)
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        lines = [
            f"1 transportation: $20",
            f"2 transportations: $50",
            f"3 transportations: $100",
            f"4 transportations: $200",
        ]
        for text_line in lines:
            p.drawText(5, current_y, text_line)
            current_y += line_height
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        # 也可加其他資訊
        p.setFont(smallFont)
        p.drawText(5, current_y, f"Mortgage {card.mortgage}")

    elif card.color == "公司":
        # 公司卡面
        # 例：1 corporation: the number of dices times 4
        #     2 corporation: the number of dices times 10
        #     3 corporation: the number of dices times 30
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
        # 也可加其他資訊
        p.setFont(smallFont)
        p.drawText(5, current_y, f"Mortgage {card.mortgage}")

    else:
        # 一般房地產卡面
        p.setFont(normalFont)
        current_y = header_h + int(height * 0.05)
        line_height = int(height * 0.06)

        p.drawText(5, current_y, f"Price {card.price}")
        current_y += line_height
        p.drawText(5, current_y, f"Rent {card.rent}")
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

    p.end()
    return pixmap


# -----------------------------------------
# 卡片Widget（小卡 + 拖曳 + 雙擊放大）
# -----------------------------------------
class CardWidget(QLabel):
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
        dialog = ZoomCardDialog(self.card, parent=self)
        dialog.exec_()


class ZoomCardDialog(QDialog):
    def __init__(self, card: Card, parent=None):
        super().__init__(parent)
        self.card = card
        self.setWindowTitle("放大卡片 - " + self.card.name)
        self.resize(500, 700)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.updateLargeCard()

    def updateLargeCard(self):
        large_size = QSize(400, 550)
        pixmap = render_card_image(self.card, large_size)
        self.label.setPixmap(pixmap)

# -----------------------------------------
# 這裡是「重點」：AreaWidget 改成
# QScrollArea + FlowLayout => 自動換行 + 可卷動
# -----------------------------------------
class AreaWidget(QScrollArea):
    """
    代表一個組 (Group1/2/3) 或 Center 區域，可以放多張卡片。
    改用 QScrollArea + FlowLayout:
      - self.container: 真正放 Widget 的母容器
      - self.flowLayout: 流式排版 => 會自動換行
    """

    def __init__(self, area_name, parent=None):
        super().__init__(parent)
        self.area_name = area_name
        self.setAcceptDrops(True)

        # 內容容器 (用 QWidget)
        self.container = QWidget()
        self.flowLayout = FlowLayout(self.container, margin=10, spacing=10)
        self.container.setLayout(self.flowLayout)

        # 如果不是Center，就在FlowLayout裡放一個「組員照片框」(僅示範)
        if self.area_name != "Center":
            photoFrame = QLabel("組員照片", self.container)
            photoFrame.setStyleSheet("background-color: #CCCCCC; border:1px solid #999;")
            photoFrame.setFixedSize(80, 80)
            # 直接加到 flowLayout
            self.flowLayout.addWidget(photoFrame)

        # 把 container 放進 QScrollArea
        self.setWidget(self.container)
        self.setWidgetResizable(True)

    # ---- 拖曳相關 ----
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

            # 從舊的容器移除
            old_parent = source_widget.parent()
            if isinstance(old_parent, AreaWidget):
                old_parent.flowLayout.removeWidget(source_widget)

            # 加到新的 flowLayout
            self.flowLayout.addWidget(source_widget)

            # 重新排序
            self.sortByColor()

            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def sortByColor(self):
        """
        按顏色排序：FlowLayout要自己拿出所有widget -> sort -> 再加回
        但要注意photoFrame(若存在)應該保留在最前
        """
        # 先把 widget 全部取出
        tempList = []
        for i in range(self.flowLayout.count()):
            item = self.flowLayout.itemAt(i)
            w = item.widget()
            tempList.append(w)

        # 如果第一個是 photoFrame，就先取出來
        photoFrame = None
        if self.area_name != "Center" and len(tempList) > 0:
            # 假設我們固定把第一個視為 photoFrame
            photoFrame = tempList[0]
            cardWidgets = tempList[1:]
        else:
            cardWidgets = tempList

        # 排序 cardWidgets
        def color_key(w):
            c = w.card.color
            try:
                return COLOR_ORDER.index(c)
            except ValueError:
                return len(COLOR_ORDER)

        cardWidgets = [w for w in cardWidgets if isinstance(w, CardWidget)]
        cardWidgets.sort(key=color_key)

        # 重新加回 flowLayout
        for i in range(self.flowLayout.count()):
            self.flowLayout.takeAt(0)  # 不斷pop

        if photoFrame:
            self.flowLayout.addWidget(photoFrame)

        for w in cardWidgets:
            self.flowLayout.addWidget(w)

# -----------------------------------------
# 主視窗
# -----------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.setWindowTitle("大富翁卡片 (FlowLayout + ScrollArea)")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # 左：三個 Group (AreaWidget)
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
        main_layout.addWidget(self.center_area, stretch=2)

        # 建立幾張卡片
        self.cards = [
            Card(name="小港", color="咖啡", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="大寮", color="咖啡", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="左營高鐵站", color="交通", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="清水", color="淺藍", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="台中遠雄", color="淺藍", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="烏日", color="淺藍", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="夢時代", color="粉", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="純文實業", color="公司", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="鳳山", color="粉", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="海港", color="粉", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="桃園機場", color="交通", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="中央大學", color="橘", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="白帥帥新光店", color="橘", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="義大飯店", color="橘", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="白帥帥興中店", color="紅", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="台灣大學", color="紅", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="北師大", color="紅", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="台北高鐵站", color="交通", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="海洋大學", color="黃", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="薇閣中學", color="黃", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="洪志淳皮膚科", color="公司", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="天母", color="黃", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="昭明國小", color="綠", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="信義國小", color="綠", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="蒲園", color="綠", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="阿姆斯特丹機場", color="交通", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="SMG", color="藍", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
            Card(name="KaaK Group", color="公司", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),     
            Card(name="倫敦", color="藍", price="$60", rent="$2",
                 house_rents=["$10","$20","$40","$80"], hotel_rent="$120",house_cost="$50",mortgage="$25"),
        ]
        

        # 新增到 Center
        for c in self.cards:
            w = CardWidget(c)
            self.center_area.flowLayout.addWidget(w)

        self.center_area.sortByColor()

# -----------------------------------------
# 執行
# -----------------------------------------
def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
