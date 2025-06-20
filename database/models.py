# классы для базы данных

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class User:
    user_id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    registration_date: datetime

@dataclass
class Order:
    order_id: int
    user_id: int
    items: List[Dict]  # Список товаров
    total: float
    address: str
    status: str  # 'new', 'processing', 'completed', 'cancelled'
    order_date: datetime

@dataclass
class MenuItem:
    item_id: int
    name: str
    description: str
    price: float
    category: str
    available: bool