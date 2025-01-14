import tkinter as tk
from tkinter import font

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

class PropertyCard(tk.Frame):
    def __init__(
        self, master,
        property_name="New York Ave",
        price="$210",
        rent="$14",
        house_rents=None,   # 1~4 houses, e.g. ["$10", "$20", "$40", "$80"]
        hotel_rent="$120",
        house_cost="$30",
        mortgage="$25",
        color="橘",        # 預設顏色
        *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        # 若 house_rents 沒有傳入，就給預設值
        if house_rents is None:
            house_rents = ["$10", "$20", "$40", "$80"]

        # 取得對應顏色的 hex
        bg_color = COLOR_MAP.get(color, "#f39423")  # 若字典裡找不到就用橘色

        # 設定整張卡片的邊框、背景色等外觀
        self.config(
            highlightthickness=2, 
            highlightbackground="black", 
            width=200, 
            height=300
        )
        
        # 自訂一些字型(可自行調整)
        self.title_font = font.Font(family="Arial", size=14, weight="bold")
        self.label_font = font.Font(family="Arial", size=10)
        self.small_font = font.Font(family="Arial", size=9)

        # ==============
        #  1. 上方色塊 (地產名稱)
        # ==============
        self.header_frame = tk.Frame(self, bg=bg_color, width=200, height=40)
        self.header_frame.pack(fill="x")
        
        self.property_label = tk.Label(
            self.header_frame, 
            text=property_name, 
            bg=bg_color, 
            fg="white",
            font=self.title_font
        )
        self.property_label.pack(pady=5)

        # ==============
        #  2. 中間區域 (價格、房租列表)
        # ==============
        self.body_frame = tk.Frame(self, bg="white")
        self.body_frame.pack(fill="both", expand=True)

        # 價格租金標題 (例如：Price $210, Rent $14)
        self.price_label = tk.Label(
            self.body_frame, 
            text=f"Price {price}", 
            font=self.label_font, 
            bg="white"
        )
        self.price_label.pack(pady=(10, 0))

        self.rent_label = tk.Label(
            self.body_frame, 
            text=f"Rent {rent}", 
            font=self.label_font, 
            bg="white"
        )
        self.rent_label.pack(pady=2)

        # 虛線分隔
        self._draw_dashed_line()

        # Houses rents
        self._create_rent_label("With 1 House:", house_rents[0])
        self._create_rent_label("With 2 House:", house_rents[1])
        self._create_rent_label("With 3 House:", house_rents[2])
        self._create_rent_label("With 4 House:", house_rents[3])

        # Hotel
        self._create_rent_label("With 1 Hotel:", hotel_rent)

        self._draw_dashed_line()

        # ==============
        #  3. 下方資訊 (建造房子費用、抵押等)
        # ==============
        self.house_cost_label = tk.Label(
            self.body_frame,
            text=f"One house cost {house_cost}",
            font=self.small_font,
            bg="white"
        )
        self.house_cost_label.pack(pady=2)

        self.mortgage_label = tk.Label(
            self.body_frame,
            text=f"Mortgage {mortgage}",
            font=self.small_font,
            bg="white"
        )
        self.mortgage_label.pack(pady=(0, 5))

    def _create_rent_label(self, text_title, value):
        """
        建立房租顯示的標籤
        """
        frame = tk.Frame(self.body_frame, bg="white")
        frame.pack(pady=1)
        
        title_lbl = tk.Label(
            frame,
            text=text_title,
            font=self.label_font,
            bg="white"
        )
        title_lbl.pack(side="left")

        value_lbl = tk.Label(
            frame,
            text=value,
            font=self.label_font,
            bg="white",
            fg="black"
        )
        value_lbl.pack(side="left", padx=5)

    def _draw_dashed_line(self):
        """
        用一個Label來假裝「虛線分隔」，也可考慮Canvas來繪製
        """
        line_label = tk.Label(
            self.body_frame, 
            text="-------------------------", 
            font=self.label_font,
            bg="white"
        )
        line_label.pack(pady=3)

# =============
# 測試視窗 (可自行刪除或整合到你的主程式)
# =============
if __name__ == "__main__":
    root = tk.Tk()
    root.title("大富翁房地產卡片 UI 示範")

    # 範例：顯示一張卡片
    card = PropertyCard(
        root,
        property_name="New York Ave",
        price="$210",
        rent="$14",
        house_rents=["$10", "$20", "$40", "$80"],
        hotel_rent="$120",
        house_cost="$30",
        mortgage="$25",
        color="橘"
    )
    card.pack(padx=10, pady=10)

    # 也可以多建幾張不同顏色、不同內容的卡片
    card2 = PropertyCard(
        root,
        property_name="台北車站",
        price="$300",
        rent="$30",
        house_rents=["$60", "$90", "$120", "$150"],
        hotel_rent="$200",
        house_cost="$50",
        mortgage="$100",
        color="紅"
    )
    card2.pack(padx=10, pady=10)

    root.mainloop()
