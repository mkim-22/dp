from PyQt6.QtWidgets import QDialog, QMessageBox

from view.add_order_window_ui import Ui_AddOrderWindow
from service.db_service import DBService


class AddOrderService(QDialog, Ui_AddOrderWindow):
    def __init__(self, parent=None, order=None):
        super().__init__(parent)
        self.setupUi(self)
        self.order = order

        self.db = DBService()
        self._load_references()

        if order:
            self._fill_fields(order)
            self.setWindowTitle("Редактировать заказ")
            self.add_order_btn.setText("Сохранить изменения")
        else:
            self.setWindowTitle("Добавление заказа")

        self.add_order_btn.clicked.connect(self.save_order)
        # Кнопка "Назад" — закрываем диалог без сохранения
        self.go_back_btn.clicked.connect(self.reject)

    def _load_references(self):
        refs = self.db.get_order_references_db()
        if not refs:
            return
        for id_status, name in refs["statuses"]:
            self.status_cbx.addItem(name, id_status)
        for id_point, address in refs["pick_up_points"]:
            self.pick_up_point_cbx.addItem(address, id_point)

    def _fill_fields(self, order):
        from PyQt6.QtCore import QDate
        self.status_cbx.setCurrentIndex(self.status_cbx.findData(order.id_status))
        self.pick_up_point_cbx.setCurrentIndex(self.pick_up_point_cbx.findData(order.id_pick_up_ponit))
        self.date_order_de.setDate(QDate(order.date_order.year, order.date_order.month, order.date_order.day))
        self.dat_delivery_de.setDate(QDate(order.date_delivery.year, order.date_delivery.month, order.date_delivery.day))

    def save_order(self):
        id_status = self.status_cbx.currentData()
        id_pick_up_point = self.pick_up_point_cbx.currentData()
        date_order = self.date_order_de.date().toPyDate()
        date_delivery = self.dat_delivery_de.date().toPyDate()

        if date_delivery < date_order:
            QMessageBox.warning(self, "Ошибка", "Дата доставки не может быть раньше даты заказа!")
            return

        if self.order:
            ok = self.db.update_order_db(
                self.order.id, id_status, id_pick_up_point, date_order, date_delivery
            )
            if ok:
                QMessageBox.information(self, "Успех", "Заказ успешно обновлён!")
                self.accept()
        else:
            ok = self.db.add_order_db(id_status, id_pick_up_point, date_order, date_delivery)
            if ok:
                QMessageBox.information(self, "Успех", "Заказ успешно добавлен!")
                self.accept()