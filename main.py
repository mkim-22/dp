import sys
from PyQt6.QtWidgets import QApplication

from service.auth_window_service import AuthWindowService

app = QApplication(sys.argv)
wind = AuthWindowService()
wind.show()
sys.exit(app.exec())