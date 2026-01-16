from dataclasses import dataclass
@dataclass
class Stock:
    store_id : int
    product_id : int
    quantity : int

    def __hash__(self):
        return hash(self.product_id)