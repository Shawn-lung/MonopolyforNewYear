# models.py

from typing import List, Optional

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
    """
    代表一張卡片（地產、交通、公司或特殊卡等）。
    """
    def __init__(
        self,
        name: str,
        description: str = "",
        price: str = "$0",
        rent: str = "$0",
        set_rent: str = "$0",
        house_rents: Optional[List[str]] = None,
        hotel_rent: str = "$0",
        house_cost: str = "$0",
        mortgage: str = "$0",
        unmortgage: str = "$0",
        color: str = "橘",
        group: Optional[str] = None
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
        self.is_mortgaged = False  # 是否被抵押

    def toggle_mortgage(self) -> None:
        """
        切換抵押狀態。
        """
        self.is_mortgaged = not self.is_mortgaged
