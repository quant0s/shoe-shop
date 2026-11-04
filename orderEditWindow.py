from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, QDate)
from PySide6.QtWidgets import (QComboBox, QDateEdit, QHBoxLayout, QLabel,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget, QFormLayout, QGroupBox, QLineEdit, QSizePolicy)


class Ui_OrderEditWindow(object):
    def setupUi(self, OrderEditWindow):
        if not OrderEditWindow.objectName():
            OrderEditWindow.setObjectName(u"OrderEditWindow")
        OrderEditWindow.resize(950, 600)

        self.scrollArea = QScrollArea(OrderEditWindow)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setMinimumSize(500, 250)

        self.mainLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(25, 25, 25, 25)

        self.headerLabel = QLabel(self.scrollAreaWidgetContents)
        self.headerLabel.setObjectName(u"headerLabel")
        self.headerLabel.setAlignment(Qt.AlignCenter)
        self.headerLabel.setMinimumHeight(40)
        self.mainLayout.addWidget(self.headerLabel)

        self.formGroup = QGroupBox(self.scrollAreaWidgetContents)
        self.formGroup.setObjectName(u"formGroup")
        self.formGroup.setMinimumWidth(500)

        self.formLayout = QFormLayout(self.formGroup)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSpacing(12)
        self.formLayout.setContentsMargins(20, 20, 20, 20)

        self.articleLabel = QLabel(self.formGroup)
        self.articleLabel.setObjectName(u"articleLabel")
        self.articleText = QLineEdit(self.formGroup)
        self.articleText.setObjectName(u"articleText")
        self.articleText.setMinimumHeight(25)
        self.articleText.setMinimumWidth(300)
        self.articleText.setReadOnly(True)
        self.formLayout.addRow(self.articleLabel, self.articleText)

        self.statusLabel = QLabel(self.formGroup)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusCombo = QComboBox(self.formGroup)
        self.statusCombo.setObjectName(u"statusCombo")
        self.statusCombo.setMinimumHeight(25)
        self.statusCombo.setMinimumWidth(300)
        self.statusCombo.addItems(["Новый", "В обработке", "Доставка", "Выполнен", "Отменен"])
        self.formLayout.addRow(self.statusLabel, self.statusCombo)

        self.addressLabel = QLabel(self.formGroup)
        self.addressLabel.setObjectName(u"addressLabel")
        self.addressCombo = QComboBox(self.formGroup)
        self.addressCombo.setObjectName(u"addressCombo")
        self.addressCombo.setMinimumHeight(25)
        self.addressCombo.setMinimumWidth(300)
        self.formLayout.addRow(self.addressLabel, self.addressCombo)

        self.orderDateLabel = QLabel(self.formGroup)
        self.orderDateLabel.setObjectName(u"orderDateLabel")
        self.orderDateEdit = QDateEdit(self.formGroup)
        self.orderDateEdit.setObjectName(u"orderDateEdit")
        self.orderDateEdit.setMinimumHeight(25)
        self.orderDateEdit.setMinimumWidth(300)
        self.orderDateEdit.setCalendarPopup(True)
        self.orderDateEdit.setDate(QDate.currentDate())
        self.formLayout.addRow(self.orderDateLabel, self.orderDateEdit)

        self.deliveryDateLabel = QLabel(self.formGroup)
        self.deliveryDateLabel.setObjectName(u"deliveryDateLabel")
        self.deliveryDateEdit = QDateEdit(self.formGroup)
        self.deliveryDateEdit.setObjectName(u"deliveryDateEdit")
        self.deliveryDateEdit.setMinimumHeight(25)
        self.deliveryDateEdit.setMinimumWidth(300)
        self.deliveryDateEdit.setCalendarPopup(True)
        self.deliveryDateEdit.setDate(QDate.currentDate().addDays(7))
        self.formLayout.addRow(self.deliveryDateLabel, self.deliveryDateEdit)

        self.mainLayout.addWidget(self.formGroup)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.buttonsLayout.setSpacing(15)

        self.saveBtn = QPushButton(self.scrollAreaWidgetContents)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setMinimumHeight(35)
        self.saveBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.buttonsLayout.addWidget(self.saveBtn)

        self.cancelBtn = QPushButton(self.scrollAreaWidgetContents)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMinimumHeight(35)
        self.cancelBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.buttonsLayout.addWidget(self.cancelBtn)

        self.deleteBtn = QPushButton(self.scrollAreaWidgetContents)
        self.deleteBtn.setObjectName(u"deleteBtn")
        self.deleteBtn.setMinimumHeight(35)
        self.deleteBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.deleteBtn.setVisible(False)
        self.buttonsLayout.addWidget(self.deleteBtn)

        self.mainLayout.addLayout(self.buttonsLayout)
        self.mainLayout.addStretch()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout = QVBoxLayout(OrderEditWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.scrollArea)

        self.setStyleSheet(OrderEditWindow)
        self.retranslateUi(OrderEditWindow)
        QMetaObject.connectSlotsByName(OrderEditWindow)

    def setStyleSheet(self, OrderEditWindow):
        OrderEditWindow.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Times New Roman';
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #7FFF00;
                color: black;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
            QPushButton#deleteBtn {
                background-color: #FF6347;
                color: white;
            }
            QPushButton#deleteBtn:hover {
                background-color: #FF4500;
            }
            QLineEdit {
                selection-background-color: #7FFF00;
                selection-color: black;
            }
            QLineEdit, QComboBox, QDateEdit {
                border: 1px solid #C2C7CB;
                border-radius: 4px;
                background-color: white;
                color: black;
                min-height: 25px;
                font-size: 13px;
            }
            QGroupBox {
                color: black;
            }
            QComboBox {
                background-color: white;
                min-width: 85px;
            }
            QComboBox:focus {
                border: 2px solid #7FFF00;
                background-color: #F8FFF8;
            }
            QComboBox QAbstractItemView {
                border-radius: 4px;
                background-color: white;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 12px;
                border: none;
                outline: none;
                background-color: transparent;
            }
            QComboBox QAbstractItemView::item:selected:active {
                border-left: 3px solid #7FFF00;
                background-color: transparent;
                color: black;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F0F0F0;
                color: black;
            }
            QDateEdit {
                selection-background-color: #7FFF00;
                selection-color: black;
            }
            QDateEdit:focus {
                background-color: #F8FFF8;
                selection-background-color: #7FFF00;
                selection-color: black;
            }
            QCalendarWidget QTableView:item:selected {
                background-color: #7FFF00;
                color: black;
            }
        """)

        self.scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 10px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #a0a0a0;
            }
        """)

        # Стиль заголовка как в товарах
        self.headerLabel.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: black;
                padding: 8px;
                margin-bottom: 5px;
                border-bottom: 1px solid #7FFF00;
            }
        """)

        self.formGroup.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #00FA9A;
                border-radius: 5px;
                padding-top: 10px;
                color: black;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: black;
            }
        """)

        self.saveBtn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: black;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
        """)

        self.cancelBtn.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
                color: black;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
        """)

        self.deleteBtn.setStyleSheet("""
            QPushButton {
                background-color: #FF6347;
                color: white;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
        """)

    def retranslateUi(self, OrderEditWindow):
        OrderEditWindow.setWindowTitle(QCoreApplication.translate("OrderEditWindow", u"Редактирование заказа", None))
        self.headerLabel.setText(QCoreApplication.translate("OrderEditWindow", u"Редактирование заказа", None))
        self.formGroup.setTitle(QCoreApplication.translate("OrderEditWindow", u"Информация о заказе", None))
        self.articleLabel.setText(QCoreApplication.translate("OrderEditWindow", u"Артикул заказа:", None))
        self.statusLabel.setText(QCoreApplication.translate("OrderEditWindow", u"Статус:", None))
        self.addressLabel.setText(QCoreApplication.translate("OrderEditWindow", u"Пункт выдачи:", None))
        self.orderDateLabel.setText(QCoreApplication.translate("OrderEditWindow", u"Дата заказа:", None))
        self.deliveryDateLabel.setText(QCoreApplication.translate("OrderEditWindow", u"Дата доставки:", None))
        self.saveBtn.setText(QCoreApplication.translate("OrderEditWindow", u"Сохранить", None))
        self.cancelBtn.setText(QCoreApplication.translate("OrderEditWindow", u"Отмена", None))
        self.deleteBtn.setText(QCoreApplication.translate("OrderEditWindow", u"Удалить", None))