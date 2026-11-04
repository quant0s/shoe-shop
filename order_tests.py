import psycopg
from datetime import date


class OrderTests:
    def __init__(self):
        self.conn = psycopg.connect(
            host="localhost",
            dbname="shoe_shop",
            user="postgres",
            password="p@ssw0rd",
            port="5432"
        )
        self.conn.autocommit = False
        self.cursor = self.conn.cursor()

    def positive_test(self):
        try:
            self.cursor.execute("SELECT id FROM pickup_points LIMIT 1")
            pickup_point = self.cursor.fetchone()[0]

            self.cursor.execute("""
                SELECT item_number
                FROM items
                WHERE quantity_stock > 0
                LIMIT 1
            """)
            item = self.cursor.fetchone()
            if not item:
                return False, "Нет товара с остатком на складе"

            item_number = item[0]

            self.cursor.execute("""
                SELECT COALESCE(MAX(order_number::int), 0) + 1 FROM orders
            """)
            order_number = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT id FROM users LIMIT 1")
            user_id = self.cursor.fetchone()[0]

            self.cursor.execute("""
                INSERT INTO orders (
                    order_number, order_date, delivery_date,
                    receipt_code, order_status, id_pickup_point, id_user
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                order_number,
                date.today(),
                date.today(),
                999,
                "Новый",
                pickup_point,
                user_id
            ))

            self.cursor.execute("""
                INSERT INTO orders_items (order_number, item_number, quantity)
                VALUES (%s, %s, 1)
            """, (order_number, item_number))

            self.cursor.execute("""
                UPDATE items
                SET quantity_stock = quantity_stock - 1
                WHERE item_number = %s
            """, (item_number,))

            self.conn.commit()
            return True, f"Заказ №{order_number} успешно добавлен"

        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def negative_test(self):
        try:
            self.cursor.execute("SELECT id FROM pickup_points LIMIT 1")
            pickup_point = self.cursor.fetchone()[0]

            self.cursor.execute("""
                SELECT COALESCE(MAX(order_number::int), 0) + 1 FROM orders
            """)
            order_number = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT id FROM users LIMIT 1")
            user_id = self.cursor.fetchone()[0]

            self.cursor.execute("""
                INSERT INTO orders (
                    order_number, order_date, delivery_date,
                    receipt_code, order_status, id_pickup_point, id_user
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                order_number,
                date.today(),
                date.today(),
                888,
                "Новый",
                pickup_point,
                user_id
            ))

            raise Exception("Заказ не может быть создан без товаров")

        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def close(self):
        self.cursor.close()
        self.conn.close()
