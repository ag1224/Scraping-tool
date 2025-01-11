import os
import json
from abc import ABC, abstractmethod
from typing import List
from models import Product

class Storage(ABC):
    @abstractmethod
    def load_data(self) -> List[Product]:
        pass

    @abstractmethod
    def save_data(self, products: List[Product]) -> None:
        pass

class JSONStorage(Storage):
    def __init__(self, filepath: str = "products.json"):
        self.filepath = filepath

    def load_data(self) -> List[Product]:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Product(**item) for item in data]

    def save_data(self, products: List[Product]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([product.model_dump() for product in products], f, ensure_ascii=False, indent=4)
