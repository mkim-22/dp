from datetime import date
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from service.db_service import DBService
from view.orders_window_ui import Ui_OrdersWindow


class OrdersWindowService(QWidget, Ui_OrdersWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.user = user

        self._reload_orders()

        if self.user.id_role == 1:
            self.open_add_order_window_btn.clicked.connect(self.open_add_order_window)
        else:
            self.open_add_order_window_btn.hide()

        self.go_back_btn.clicked.connect(lambda: self.open_product_wind(self.user))

    def display_order(self, order_list):
        old = self.scrollArea.takeWidget()
        if old:
            old.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.order_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.order_layout)

        for order in order_list:
            order_widget = QWidget()
            order_layout = QHBoxLayout()
            order_widget.setLayout(order_layout)
            self.order_layout.addWidget(order_widget)

            order_info_l = QLabel(
                f"Номер заказа: {order.id}\n"
                f"Статус заказа: {order.status_name}\n"
                f"Адрес пункта выдачи: {order.id_pick_up_ponit_name}\n"
                f"Дата заказа: {date.strftime(order.date_order, '%d.%m.%Y')}\n"
            )
            order_info_l.setWordWrap(True)
            order_info_l.setFixedHeight(200)
            order_info_l.setStyleSheet("border: 1px solid black")
            order_layout.addWidget(order_info_l)

            order_date_delivery_l = QLabel(
                f"Дата доставки\n{date.strftime(order.date_delivery, '%d.%m.%Y')}"
            )
            order_date_delivery_l.setWordWrap(True)
            order_date_delivery_l.setFixedHeight(200)
            order_date_delivery_l.setStyleSheet("border: 1px solid black")
            order_date_delivery_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            order_layout.addWidget(order_date_delivery_l)

            if self.user.id_role == 1:
                edit_btn = QPushButton("Редактировать")
                edit_btn.setFixedHeight(40)
                edit_btn.clicked.connect(lambda ch, o=order: self.open_edit_order_window(o))
                order_layout.addWidget(edit_btn)

                del_btn = QPushButton("Удалить")
                del_btn.setFixedHeight(40)
                del_btn.setStyleSheet("background-color: #FF6B6B;")
                del_btn.clicked.connect(lambda ch, oid=order.id: self.delete_order(oid))
                order_layout.addWidget(del_btn)

    def open_add_order_window(self):
        from service.add_order import AddOrderService
        dialog = AddOrderService(self)
        if dialog.exec():
            self._reload_orders()

    def open_edit_order_window(self, order):
        from service.add_order import AddOrderService
        dialog = AddOrderService(self, order)
        if dialog.exec():
            self._reload_orders()

    def delete_order(self, id_order):
        DBService().delete_order_db(id_order)
        self._reload_orders()

    def _reload_orders(self):
        # Каждый раз создаём новый DBService() — новое соединение,
        # чтобы pymysql не отдавал закэшированные данные старой транзакции
        order_list = DBService().get_orders_info_db()
        if order_list:
            self.display_order(order_list)

    def open_product_wind(self, user):
        from service.products_window_service import ProductsWindowService
        self.wind = ProductsWindowService(user)
        self.wind.show()
        self.close()