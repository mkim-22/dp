from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from service.db_service import DBService
from view.products_window_ui import Ui_ProductsWindow

class ProductsWindowService(QWidget, Ui_ProductsWindow):
    def __init__(self, user=None):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("data/Icon.png"))
        self.logo_I.setPixmap(QPixmap("data/Icon.png"))

        self.user = user
        self.product_list = DBService().get_products_info_db()

        if self.product_list:
            self.display_products(self.product_list)

            # добавление в выпадаюший список фильтрации уникльных пар поставщиков
            suppliers_dict = {product.id_suppliers: product.suppliers_name for product in self.product_list}
            self.filter_cbx.addItem("Все поставщики", 0)
            for supplier_id, supplier_name in suppliers_dict.items():
                self.filter_cbx.addItem(supplier_name, supplier_id)

            self.sort_cbx.addItem("Без сортировки", 0)
            self.sort_cbx.addItem("По возрастанию", 1)
            self.sort_cbx.addItem("По убыванию", 2)

        # Если ползьователь авторизован, то имя отображается в правом верхенм углу
        if self.user:
            self.user_name_I.setText(f"{self.user.last_name} {self.user.first_name} {self.user.pataranomic}")

        # Если пользователь на авторизован, или не является админом или менеджером
        # то ему не доступны сортировка, фильтрация и посик
        if not self.user or not self.user.id_role in (1, 2):
            self.filter_cbx.hide()
            self.sort_cbx.hide()
            self.search_le.hide()
            self.open_orders_window_btn.hide()

        # Кнопка добавления товара — только для админа (id_role = 1)
        if self.user and self.user.id_role == 1:
            self.add_product_btn.clicked.connect(self.open_add_product)
        else:
            self.add_product_btn.hide()

        self.sort_cbx.currentIndexChanged.connect(lambda: self.search_filter_sort())
        self.filter_cbx.currentIndexChanged.connect(lambda: self.search_filter_sort())
        self.search_le.textChanged.connect(lambda: self.search_filter_sort())

        self.open_orders_window_btn.clicked.connect(lambda: self.open_orders_window(self.user))

        self.go_back_btn.clicked.connect(lambda: self.exit())

    def display_products(self, product_list):
        old = self.scrollArea.takeWidget()
        if old:
            old.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.product_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.product_layout)

        for product in product_list:
            product_widget = QWidget()
            product_layout = QHBoxLayout()
            product_widget.setLayout(product_layout)
            self.product_layout.addWidget(product_widget)

            if product.discount > 0:
                disc_price = round(product.price * (1 - product.discount / 100),2)
                price_text = f"<s style= 'color: red'>{product.price}</s> {disc_price}"
            else:
                price_text = str(product.price)

            if product.discount > 15:
                product_widget.setStyleSheet("background-color: #2E8B57")


            product_photo_l = QLabel()
            product_photo_l.setFixedSize(200, 200)
            product_photo_l.setStyleSheet("border: 1px solid black")
            photo = product.photo if product.photo else QPixmap("data/picture.png")
            product_photo_l.setPixmap(photo.scaled(product_photo_l.size()))
            product_layout.addWidget(product_photo_l)

            product_info_l = QLabel(f"{product.article}<br>"
                f"{product.category_name} | {product.type_name}<br>"
                                     f"Описание товара: {product.descrition}<br>"
                                     f"Производитель: {product.producer_name}"
                                     f"Поставщик: {product.suppliers_name}<br>"
                                     f"Цена: {price_text}<br>"
                                     f"Единица измерения: {product.unit}<br>"
                                     f"Кол-во на складе: {product.amount_storage}")

            product_info_l.setWordWrap(True)
            product_info_l.setFixedHeight(200)
            product_info_l.setStyleSheet("border: 1px solid black")
            product_layout.addWidget(product_info_l)


            product_discount_l = QLabel(f"Действующая скидка: \n {product.discount}%")
            product_discount_l.setWordWrap(True)
            product_discount_l.setFixedHeight(200)
            product_discount_l.setStyleSheet("border: 1px solid black")
            product_discount_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            product_layout.addWidget(product_discount_l)

            if self.user and self.user.id_role == 1:
                edit_btn = QPushButton("Редактировать")
                edit_btn.clicked.connect(lambda ch, p=product: self.open_edit_product(p))
                product_layout.addWidget(edit_btn)

                del_btn = QPushButton("Удалить")
                del_btn.clicked.connect(lambda ch, sid=product.id: self.delete(sid))
                product_layout.addWidget(del_btn)

    def search_filter_sort(self):
        search_words = self.search_le.text().lower().split()
        filter_option = self.filter_cbx.currentData()
        sort_option = self.sort_cbx.currentData()

        filtered_products = self.product_list
        # Поиск
        if search_words:
            filtered_products = [p for p in filtered_products if all(word in
                                f"{p.article} {p.type_name} {p.suppliers_name} {p.producer_name} "
                                f"{p.category_name} {p.descrition}".lower() for word in search_words)]
        # Фильтрация по поставщику
        if filter_option != 0:
            filtered_products = [product for product in filtered_products if
                                 product.id_suppliers == filter_option]

        # Сортировка
        if sort_option != 0:
            filtered_products = sorted(filtered_products, key=lambda product: product.amount_storage,
                                       reverse=False if sort_option == 1 else True)

        self.display_products(filtered_products)


    def open_add_product(self):
        from service.add_product_service import AddProductService
        dialog = AddProductService(self)
        if dialog.exec():
            # Перезагружаем список товаров после добавления
            self.product_list = DBService().get_products_info_db()
            if self.product_list:
                self.display_products(self.product_list)


    def open_edit_product(self, product):
        from service.add_product_service import AddProductService
        dialog = AddProductService(self, product)
        if dialog.exec():
            self.product_list = DBService().get_products_info_db()
            if self.product_list:
                self.display_products(self.product_list)


    def delete(self, id_service):
        DBService().delete(id_service)
        self.product_list = DBService().get_products_info_db()
        self.display_products(self.product_list)

    def exit(self):
        from service.auth_window_service import AuthWindowService
        self.wind = AuthWindowService()
        self.wind.show()
        self.close()

    def open_orders_window(self, user):
        from service.orders_window_service import OrdersWindowService
        self.wind = OrdersWindowService(user)
        self.wind.show()
        self.close()