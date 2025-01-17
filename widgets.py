# widgets.py

import sys, os
from PyQt5.QtWidgets import (
    QLabel, QScrollArea, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QFont, QColor

from flowlayout import FlowLayout
from models import Card, COLOR_MAP, COLOR_ORDER

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def render_card_image(card: Card, size: QSize, mortgaged: bool) -> QPixmap:
    """
    根據卡片資料繪製卡片（正常狀態或抵押狀態）。
    """
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.Antialiasing)

    width = size.width()
    height = size.height()

    title_font_size = int(height * 0.07)
    normal_font_size = int(height * 0.05)
    small_font_size = int(height * 0.04)

    titleFont = QFont("Arial", title_font_size, QFont.Bold)
    normalFont = QFont("Arial", normal_font_size)
    smallFont = QFont("Arial", small_font_size)

    header_h = int(height * 0.18)

    if mortgaged:
        # 抵押狀態
        p.setBrush(QColor("#7d7d7d"))  # 暗灰色背景
        p.setPen(Qt.NoPen)
        p.drawRect(0, 0, width, height)

        p.setPen(Qt.white)
        p.setFont(titleFont)
        p.drawText(0, 0, width, header_h, Qt.AlignCenter, card.name)

        p.setFont(normalFont)
        current_y = header_h + int(height * 0.10)
        line_height = int(height * 0.06)
        p.drawText(5, current_y, "--------------------------------")
        current_y += line_height
        p.drawText(5, current_y, f"抵押: {card.mortgage}")
        current_y += line_height
        p.drawText(5, current_y, f"贖回: {card.unmortgage}")
        current_y += line_height
        p.drawText(5, current_y, "--------------------------------")

    else:
        # 正常狀態
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

        # 交通公司特殊繪法
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
            # 監獄卡：簡單描述
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
    """
    卡片縮圖 + 拖曳 + 雙擊放大。
    """
    def __init__(self, card: Card, parent=None):
        super().__init__(parent)
        self.card = card
        self.drag_start_pos = QPoint()
        self.normal_size = QSize(160, 220)
        self.updateCardAppearance()

    def updateCardAppearance(self) -> None:
        """
        根據抵押狀態更新外觀。
        """
        pixmap = render_card_image(self.card, self.normal_size, self.card.is_mortgaged)
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
            from dialogs import ZoomCardDialog  # 避免循環匯入
            dialog = ZoomCardDialog(card_widget=self, card=self.card, parent=self)
            dialog.exec_()
        super().mouseDoubleClickEvent(event)

    def startDrag(self) -> None:
        """
        開始拖曳動作。
        """
        if not self.card.is_mortgaged:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.card.name)
            drag.setMimeData(mime_data)

            drag_pixmap = self.pixmap().copy()
            drag.setPixmap(drag_pixmap)
            _ = drag.exec_(Qt.MoveAction)

    def toggle_mortgage(self) -> None:
        """
        切換抵押狀態。
        """
        self.card.toggle_mortgage()
        self.updateCardAppearance()

class AreaWidget(QScrollArea):
    """
    一個區域 (Group1/2/3 或 Center)，可放多張卡片 (CardWidget)。
    使用 FlowLayout 來自動換行。
    """
    def __init__(self, area_name: str, parent=None):
        super().__init__(parent)
        self.area_name = area_name
        self.setAcceptDrops(True)

        self.container = QWidget()
        self.flowLayout = FlowLayout(self.container, margin=10, spacing=10)
        self.container.setLayout(self.flowLayout)

        # 如果不是 Center，就插入圖片(例如組員照片)示範
        if self.area_name != "Center":
            photoFrame = QLabel(self.container)
            photoFrame.setStyleSheet("border:1px solid #999;")
            photoFrame.setFixedSize(80, 80)

            image_path = image_path = resource_path(os.path.join('img', area_name + ".png"))
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
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

            # 從舊容器移除
            old_parent = source_widget.parent()
            if isinstance(old_parent, AreaWidget):
                old_parent.flowLayout.removeWidget(source_widget)

            # 加入本容器
            self.flowLayout.addWidget(source_widget)
            self.sortByColor()
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def sortByColor(self) -> None:
        """
        根據 color 排序顯示。
        """
        tempList = []
        for i in range(self.flowLayout.count()):
            item = self.flowLayout.itemAt(i)
            w = item.widget()
            tempList.append(w)

        photoFrame = None
        if self.area_name != "Center" and len(tempList) > 0:
            # 第一個可能是區域示意圖
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

        # 先清空整個 flowLayout
        for _ in range(self.flowLayout.count()):
            self.flowLayout.takeAt(0)

        # 先放回示意圖
        if photoFrame:
            self.flowLayout.addWidget(photoFrame)
        # 再放排序後的卡片
        for w in cardWidgets:
            self.flowLayout.addWidget(w)
