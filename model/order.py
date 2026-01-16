import datetime
from dataclasses import dataclass
@dataclass
class Order:
    id : int
    customer_id : int
    order_status : int
    order_date : datetime.date
    required_date : datetime.date
    shipped_date : datetime.date
    store_id : int
    staff_id : int


    def __str__(self):
        return f"{self.customer_id} {self.order_status} {self.order_date}"

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.order_date < other.order_date