from PyQt6.QtWidgets import QDialog, QMessageBox

from view.add_product_ui import Ui_AddProductDialog
from service.db_service import DBService

class AddProductService(QDialog, Ui_AddProductDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setupUi(self)
        self.product = product

        self.db = DBService()
        self._load_references()

        if product:
            self._fill_fields(product)
            self.setWindowTitle("Редактировать товар")
            self.title_lbl.setText("Редактирование товара")

        self.save_btn.clicked.connect(lambda: self.save_product())
        self.cancel_btn.clicked.connect(lambda: self.reject())

    def _load_references(self):
        refs = self.db.get_references_db()
        if not refs:
            return

        for id_type, name in refs["types"]:
            self.type_cbx.addItem(name, id_type)

        for id_sup, name in refs["suppliers"]:
            self.supplier_cbx.addItem(name, id_sup)

        for id_prod, name in refs["producers"]:
            self.producer_cbx.addItem(name, id_prod)

        for id_cat, name in refs["categories"]:
            self.category_cbx.addItem(name, id_cat)

    def _fill_fields(self, product):
        self.article_le.setText(product.article)
        self.price_sb.setValue(product.price)
        self.discount_sb.setValue(product.discount)
        self.amount_sb.setValue(product.amount_storage)
        self.desc_le.setText(product.descrition or "")
        self.photo_le.setText(product.photo_name or "")
        self.type_cbx.setCurrentIndex(self.type_cbx.findData(product.id_type))
        self.supplier_cbx.setCurrentIndex(self.supplier_cbx.findData(product.id_suppliers))
        self.producer_cbx.setCurrentIndex(self.producer_cbx.findData(product.id_producer))
        self.category_cbx.setCurrentIndex(self.category_cbx.findData(product.id_category))

    def save_product(self):
        article = self.article_le.text().strip()
        if not article:
            QMessageBox.warning(self, "Ошибка", "Артикул обязателен!")
            return
        unit = "шт"
        id_type = self.type_cbx.currentData()
        id_supplier = self.supplier_cbx.currentData()
        id_producer = self.producer_cbx.currentData()
        id_category = self.category_cbx.currentData()
        price = self.price_sb.value()
        discount = self.discount_sb.value()
        amount = self.amount_sb.value()
        desc = self.desc_le.text().strip()
        photo = self.photo_le.text().strip() or None

        if self.product:
            ok = self.db.update_product_db(self.product.id, article, id_type, unit, price,
                                           id_supplier, id_producer, id_category, discount, amount, desc, photo)
            if ok:
                QMessageBox.information(self, "Успех", "Товар успешно обновлён!")
                self.accept()
        else:
            ok = self.db.add_product_db(article, id_type, unit, price, id_supplier,
                                        id_producer, id_category, discount, amount, desc, photo)
            if ok:
                QMessageBox.information(self, "Успех", "Товар успешно добавлен!")
                self.accept()
