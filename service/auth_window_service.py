from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox

from view.auth_window_ui import Ui_AuthorizationWindow
from service.db_service import DBService

class AuthWindowService(QWidget, Ui_AuthorizationWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.auth_btn.clicked.connect(lambda: self.auth())
        self.guest_btn.clicked.connect(lambda: self.open_products_window())

    def auth(self):
        login = self.login_le.text().strip()
        password = self.password_le.text().strip()

        if not login or not password:
            QMessageBox.warning(None, "Ошибка Авторизации" , "Неверынй логин или пароль")

        user = DBService().get_user_info_db(login, password)
        if user:
            self.open_products_window(user)
        return None

    def open_products_window(self, user=None):
        from service.products_window_service import ProductsWindowService
        self.wind = ProductsWindowService(user)
        self.wind.show()
        self.close()