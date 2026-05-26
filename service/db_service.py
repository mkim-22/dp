import pymysql
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox

from data.Order import Order
from data.product import Product
from data.user import User


class DBService:
    def __init__(self):
        self.conn = None
        try:
            self.conn = pymysql.connect(host="localhost", user="root", password="", database="boots_store")
        except Exception as e:
            QMessageBox.warning(None, "Ошикба подключения", f"Ошибка {e}")


    # Получение информации о пользователе из бд
    def get_user_info_db(self, login, password):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT u.id_user, u.last_name, u.first_name, u.pataranomic, u.id_role, 
                r.name from users u
                join users_roles r on r.id_role = u.id_role
                WHERE u.login = %s AND u.password = %s""", (str(login), str(password)))
                result = cur.fetchall()
                """возвраащет объект User по логину и паролю"""
                if result:
                    return User(*result[0])
                else:
                    QMessageBox.warning(None, "Ошибка авторизации", "Неверный логин или пароль")
                    return False
        except Exception as e:
            QMessageBox.warning(None, "Ошикбка получения данных", f"Ошибка {e}")
            return False


    def get_products_info_db(self):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT p.id_product, p.article, p.id_type, t.name, p.unit, p.price, p.id_suppliers, 
                s.name, p.id_producer, pr.name, p.id_category, c.name, p.discount, p.amount_storage, 
                p.descrition, p.photo FROM products p
                JOIN type_products t on t.id_type  = p.id_type
                JOIN suppliers s on s.id_suppliers = p.id_suppliers
                JOIN producer pr on pr.id_producer = p.id_producer
                JOIN category_products c on c.id_category = p.id_category""")
                result = cur.fetchall()
                product_list = []

                if result:
                    for product in result:
                        photo_name = product[15] or ""
                        photo_pixmap = QPixmap(f"data/{photo_name}") if photo_name else None
                        product_list.append(Product(*product[:15], photo_pixmap, photo_name))
                    return product_list
                else:
                    QMessageBox.warning(None, "Ошибка получения данных", "Товары не найдены")
                    return False

        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка{e}")
            return False

    def get_references_db(self):
        """Возвращает словарь со списками для комбобоксов: типы, поставщики, производители, категории"""
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id_type, name FROM type_products")
                types = cur.fetchall()
                cur.execute("SELECT id_suppliers, name FROM suppliers")
                suppliers = cur.fetchall()
                cur.execute("SELECT id_producer, name FROM producer")
                producers = cur.fetchall()
                cur.execute("SELECT id_category, name FROM category_products")
                categories = cur.fetchall()
                return {"types": types, "suppliers": suppliers,
                        "producers": producers, "categories": categories}
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка загрузки справочников: {e}")
            return None

    def add_product_db(self, article, id_type, unit, price, id_suppliers,
                       id_producer, id_category, discount, amount_storage, descrition, photo):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO products
                    (article, id_type, unit, price, id_suppliers, id_producer,
                     id_category, discount, amount_storage, descrition, photo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (article, id_type, unit, price, id_suppliers, id_producer,
                     id_category, discount, amount_storage, descrition, photo))
                self.conn.commit()
                return True
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка добавления товара: {e}")
            return False

    def update_product_db(self, id_product, article, id_type, unit, price, id_suppliers,
                          id_producer, id_category, discount, amount_storage, descrition, photo):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""UPDATE products SET article=%s, id_type=%s, unit=%s, price=%s,
                    id_suppliers=%s, id_producer=%s, id_category=%s, discount=%s,
                    amount_storage=%s, descrition=%s, photo=%s
                    WHERE id_product=%s""",
                    (article, id_type, unit, price, id_suppliers, id_producer,
                     id_category, discount, amount_storage, descrition, photo, id_product))
                self.conn.commit()
                return True
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка обновления товара: {e}")
            return False

    def delete(self, id):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""DELETE FROM products WHERE id_product = %s""", (id, ))
                self.conn.commit()
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")
            return False


    def get_orders_info_db(self):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT o.id_order, o.id_status, ors.name, o.id_pick_up_ponit,
                    concat_ws(" ", p.index, p.city, p.street, p.house),
                    o.date_order, o.date_delivery FROM orders o
                    JOIN order_status ors on ors.id_status = o.id_status
                    JOIN pick_up_points p on p.id_point = o.id_pick_up_ponit
                    ORDER BY o.id_order ASC""")
                result =  cur.fetchall()
                order_list = []
                if result:
                    for order in result:
                        order_list.append(Order(*order))
                    return order_list
                else:
                    QMessageBox.warning(None, "Ошибка", "Заказ не найден")
                    return False

        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка{e}")
            return False


    def get_order_references_db(self):
        """Возвращает словарь со списками для комбобоксов: статусы и пункты выдачи"""
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id_status, name FROM order_status")
                statuses = cur.fetchall()
                cur.execute("""SELECT id_point, CONCAT_WS(' ', `index`, city, street, house)
                               FROM pick_up_points""")
                pick_up_points = cur.fetchall()
                return {"statuses": statuses, "pick_up_points": pick_up_points}
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка загрузки справочников заказа: {e}")
            return None

    def add_order_db(self, id_status, id_pick_up_point, date_order, date_delivery):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO orders
                    (id_status, id_pick_up_ponit, date_order, date_delivery)
                    VALUES (%s, %s, %s, %s)""",
                    (id_status, id_pick_up_point, date_order, date_delivery))
                self.conn.commit()
                return True
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка добавления заказа: {e}")
            return False

    def update_order_db(self, id_order, id_status, id_pick_up_point, date_order, date_delivery):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""UPDATE orders SET
                    id_status=%s, id_pick_up_ponit=%s,
                    date_order=%s, date_delivery=%s
                    WHERE id_order=%s""",
                    (id_status, id_pick_up_point, date_order, date_delivery, id_order))
                self.conn.commit()
                return True
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка обновления заказа: {e}")
            return False

    def delete_order_db(self, id_order):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM orders WHERE id_order = %s", (id_order,))
                self.conn.commit()
                return True
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка удаления заказа: {e}")
            return False


