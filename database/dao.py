from database.DB_connect import DBConnect
from model.category import Category
from model.order import Order
from model.order_item import OrderItem
from model.product import Product
from model.stock import Stock


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def read_all_categories():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from `category`"""
        cursor.execute(query)
        for row in cursor:
            results.append(Category(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def read_all_stocks():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from `stock`"""
        cursor.execute(query)
        for row in cursor:
            results.append(Stock(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def read_all_products():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from `product`"""
        cursor.execute(query)
        for row in cursor:
            results.append(Product(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def read_all_orders():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from `order`"""
        cursor.execute(query)
        for row in cursor:
            results.append(Order(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def read_all_orders_items():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from `order_item`"""
        cursor.execute(query)
        for row in cursor:
            results.append(OrderItem(**row))
        cursor.close()
        conn.close()
        return results









