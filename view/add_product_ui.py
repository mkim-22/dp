from PyQt6 import QtCore, QtWidgets


class Ui_AddProductDialog(object):
    def setupUi(self, AddProductDialog):
        AddProductDialog.setObjectName("AddProductDialog")
        AddProductDialog.resize(420, 560)
        AddProductDialog.setStyleSheet(
            "QWidget{background-color: #FFFFFF; font-family: \"Times New Roman\"; font-size: 12pt; color: black}"
            "QLineEdit{border: 1px solid black; padding: 2px;}"
            "QComboBox{border: 1px solid black;}"
            "QSpinBox{border: 1px solid black;}"
            "QPushButton{background-color: #00FA9A; padding: 6px;}"
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(AddProductDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.title_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        self.article_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.article_lbl.setObjectName("article_lbl")
        self.article_le = QtWidgets.QLineEdit(parent=AddProductDialog)
        self.article_le.setObjectName("article_le")
        self.formLayout.addRow(self.article_lbl, self.article_le)

        self.type_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.type_lbl.setObjectName("type_lbl")
        self.type_cbx = QtWidgets.QComboBox(parent=AddProductDialog)
        self.type_cbx.setObjectName("type_cbx")
        self.formLayout.addRow(self.type_lbl, self.type_cbx)

        self.price_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.price_lbl.setObjectName("price_lbl")
        self.price_sb = QtWidgets.QSpinBox(parent=AddProductDialog)
        self.price_sb.setMaximum(9999999)
        self.price_sb.setObjectName("price_sb")
        self.formLayout.addRow(self.price_lbl, self.price_sb)

        self.supplier_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.supplier_lbl.setObjectName("supplier_lbl")
        self.supplier_cbx = QtWidgets.QComboBox(parent=AddProductDialog)
        self.supplier_cbx.setObjectName("supplier_cbx")
        self.formLayout.addRow(self.supplier_lbl, self.supplier_cbx)

        self.producer_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.producer_lbl.setObjectName("producer_lbl")
        self.producer_cbx = QtWidgets.QComboBox(parent=AddProductDialog)
        self.producer_cbx.setObjectName("producer_cbx")
        self.formLayout.addRow(self.producer_lbl, self.producer_cbx)

        self.category_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.category_lbl.setObjectName("category_lbl")
        self.category_cbx = QtWidgets.QComboBox(parent=AddProductDialog)
        self.category_cbx.setObjectName("category_cbx")
        self.formLayout.addRow(self.category_lbl, self.category_cbx)

        self.discount_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.discount_lbl.setObjectName("discount_lbl")
        self.discount_sb = QtWidgets.QSpinBox(parent=AddProductDialog)
        self.discount_sb.setMaximum(100)
        self.discount_sb.setObjectName("discount_sb")
        self.formLayout.addRow(self.discount_lbl, self.discount_sb)

        self.amount_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.amount_lbl.setObjectName("amount_lbl")
        self.amount_sb = QtWidgets.QSpinBox(parent=AddProductDialog)
        self.amount_sb.setMaximum(999999)
        self.amount_sb.setObjectName("amount_sb")
        self.formLayout.addRow(self.amount_lbl, self.amount_sb)

        self.desc_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.desc_lbl.setObjectName("desc_lbl")
        self.desc_le = QtWidgets.QLineEdit(parent=AddProductDialog)
        self.desc_le.setObjectName("desc_le")
        self.formLayout.addRow(self.desc_lbl, self.desc_le)

        self.photo_lbl = QtWidgets.QLabel(parent=AddProductDialog)
        self.photo_lbl.setObjectName("photo_lbl")
        self.photo_le = QtWidgets.QLineEdit(parent=AddProductDialog)
        self.photo_le.setObjectName("photo_le")
        self.formLayout.addRow(self.photo_lbl, self.photo_le)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.save_btn = QtWidgets.QPushButton(parent=AddProductDialog)
        self.save_btn.setObjectName("save_btn")
        self.cancel_btn = QtWidgets.QPushButton(parent=AddProductDialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setStyleSheet("background-color: #FF6B6B;")
        self.buttons_layout.addWidget(self.save_btn)
        self.buttons_layout.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.buttons_layout)

        self.retranslateUi(AddProductDialog)

    def retranslateUi(self, AddProductDialog):
        _translate = QtCore.QCoreApplication.translate
        AddProductDialog.setWindowTitle(_translate("AddProductDialog", "Добавить товар"))
        self.title_lbl.setText(_translate("AddProductDialog", "Добавление товара"))
        self.article_lbl.setText(_translate("AddProductDialog", "Артикул:"))
        self.type_lbl.setText(_translate("AddProductDialog", "Тип товара:"))
        self.price_lbl.setText(_translate("AddProductDialog", "Цена (руб):"))
        self.supplier_lbl.setText(_translate("AddProductDialog", "Поставщик:"))
        self.producer_lbl.setText(_translate("AddProductDialog", "Производитель:"))
        self.category_lbl.setText(_translate("AddProductDialog", "Категория:"))
        self.discount_lbl.setText(_translate("AddProductDialog", "Скидка (%):"))
        self.amount_lbl.setText(_translate("AddProductDialog", "Кол-во на складе:"))
        self.desc_lbl.setText(_translate("AddProductDialog", "Описание:"))
        self.photo_lbl.setText(_translate("AddProductDialog", "Фото (имя файла):"))
        self.photo_le.setPlaceholderText(_translate("AddProductDialog", "например: 1.jpg"))
        self.save_btn.setText(_translate("AddProductDialog", "Сохранить"))
        self.cancel_btn.setText(_translate("AddProductDialog", "Отмена"))
