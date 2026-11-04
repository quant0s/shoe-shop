from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QComboBox, QSpinBox, QDoubleSpinBox,
    QFormLayout, QGroupBox, QGridLayout, QSizePolicy
)


class Ui_ProductEditWindow(object):
    def setupUi(self, ProductEditWindow):
        if not ProductEditWindow.objectName():
            ProductEditWindow.setObjectName(u"ProductEditWindow")
        ProductEditWindow.resize(950, 600)  # Еще шире окно

        self.scrollArea = QScrollArea(ProductEditWindow)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setMinimumSize(930, 580)

        self.mainLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setSpacing(15)
        self.mainLayout.setContentsMargins(25, 25, 25, 25)

        self.headerLabel = QLabel(self.scrollAreaWidgetContents)
        self.headerLabel.setObjectName(u"headerLabel")
        self.headerLabel.setAlignment(Qt.AlignCenter)
        self.headerLabel.setMinimumHeight(40)
        self.mainLayout.addWidget(self.headerLabel)

        self.mainContainer = QWidget(self.scrollAreaWidgetContents)
        self.mainContainer.setObjectName(u"mainContainer")

        self.containerLayout = QHBoxLayout(self.mainContainer)
        self.containerLayout.setSpacing(30)
        self.containerLayout.setContentsMargins(0, 0, 0, 0)

        self.formContainer = QWidget(self.mainContainer)
        self.formContainer.setObjectName(u"formContainer")

        self.formGridLayout = QGridLayout(self.formContainer)
        self.formGridLayout.setObjectName(u"formGridLayout")
        self.formGridLayout.setSpacing(12)
        self.formGridLayout.setContentsMargins(0, 0, 0, 0)
        self.formGridLayout.setColumnMinimumWidth(1, 250)
        self.formGridLayout.setColumnMinimumWidth(3, 250)

        self.setup_form_grid()

        self.containerLayout.addWidget(self.formContainer, 1)

        self.imageContainer = QWidget(self.mainContainer)
        self.imageContainer.setObjectName(u"imageContainer")
        self.imageContainer.setFixedWidth(280)

        self.imageLayout = QVBoxLayout(self.imageContainer)
        self.imageLayout.setSpacing(12)
        self.imageLayout.setContentsMargins(0, 0, 0, 0)

        self.imageLabel = QLabel(self.imageContainer)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setMinimumSize(260, 180)
        self.imageLabel.setMaximumSize(270, 190)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageLayout.addWidget(self.imageLabel)

        self.imageButtonsLayout = QVBoxLayout()
        self.imageButtonsLayout.setSpacing(8)

        self.loadImageBtn = QPushButton(self.imageContainer)
        self.loadImageBtn.setObjectName(u"loadImageBtn")
        self.loadImageBtn.setMinimumHeight(32)
        self.imageButtonsLayout.addWidget(self.loadImageBtn)

        self.clearImageBtn = QPushButton(self.imageContainer)
        self.clearImageBtn.setObjectName(u"clearImageBtn")
        self.clearImageBtn.setMinimumHeight(32)
        self.imageButtonsLayout.addWidget(self.clearImageBtn)

        self.imageLayout.addLayout(self.imageButtonsLayout)
        self.containerLayout.addWidget(self.imageContainer)

        self.mainLayout.addWidget(self.mainContainer, 1)

        self.buttonsContainer = QWidget(self.scrollAreaWidgetContents)
        self.buttonsContainer.setObjectName(u"buttonsContainer")
        self.buttonsContainer.setMinimumHeight(50)

        self.buttonsLayout = QHBoxLayout(self.buttonsContainer)
        self.buttonsLayout.setSpacing(15)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)

        self.saveBtn = QPushButton(self.buttonsContainer)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setMinimumHeight(35)
        self.saveBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.buttonsLayout.addWidget(self.saveBtn)

        self.cancelBtn = QPushButton(self.buttonsContainer)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMinimumHeight(35)
        self.cancelBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.buttonsLayout.addWidget(self.cancelBtn)

        self.mainLayout.addWidget(self.buttonsContainer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout = QVBoxLayout(ProductEditWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.scrollArea)

        self.setStyleSheet(ProductEditWindow)
        self.retranslateUi(ProductEditWindow)
        QMetaObject.connectSlotsByName(ProductEditWindow)

    def setup_form_grid(self):
        self.nameLabel = QLabel(self.formContainer)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameEdit = QLineEdit(self.formContainer)
        self.nameEdit.setObjectName(u"nameEdit")
        self.nameEdit.setMinimumHeight(26)
        self.formGridLayout.addWidget(self.nameLabel, 0, 0)
        self.formGridLayout.addWidget(self.nameEdit, 0, 1)

        self.categoryLabel = QLabel(self.formContainer)
        self.categoryLabel.setObjectName(u"categoryLabel")
        self.categoryCombo = QComboBox(self.formContainer)
        self.categoryCombo.setObjectName(u"categoryCombo")
        self.categoryCombo.setMinimumHeight(26)  # Уменьшил высоту
        self.formGridLayout.addWidget(self.categoryLabel, 1, 0)
        self.formGridLayout.addWidget(self.categoryCombo, 1, 1)

        self.descriptionLabel = QLabel(self.formContainer)
        self.descriptionLabel.setObjectName(u"descriptionLabel")
        self.descriptionEdit = QLineEdit(self.formContainer)
        self.descriptionEdit.setObjectName(u"descriptionEdit")
        self.descriptionEdit.setMinimumHeight(26)  # Уменьшил высоту
        self.formGridLayout.addWidget(self.descriptionLabel, 2, 0)
        self.formGridLayout.addWidget(self.descriptionEdit, 2, 1)

        self.manufacturerLabel = QLabel(self.formContainer)
        self.manufacturerLabel.setObjectName(u"manufacturerLabel")
        self.manufacturerCombo = QComboBox(self.formContainer)
        self.manufacturerCombo.setObjectName(u"manufacturerCombo")
        self.manufacturerCombo.setMinimumHeight(26)
        self.formGridLayout.addWidget(self.manufacturerLabel, 3, 0)
        self.formGridLayout.addWidget(self.manufacturerCombo, 3, 1)

        self.providerLabel = QLabel(self.formContainer)
        self.providerLabel.setObjectName(u"providerLabel")
        self.providerEdit = QLineEdit(self.formContainer)
        self.providerEdit.setObjectName(u"providerEdit")
        self.providerEdit.setMinimumHeight(26)
        self.formGridLayout.addWidget(self.providerLabel, 0, 2)
        self.formGridLayout.addWidget(self.providerEdit, 0, 3)

        self.priceLabel = QLabel(self.formContainer)
        self.priceLabel.setObjectName(u"priceLabel")
        self.priceEdit = QDoubleSpinBox(self.formContainer)
        self.priceEdit.setObjectName(u"priceEdit")
        self.priceEdit.setMinimumHeight(26)
        self.priceEdit.setMinimum(0)
        self.priceEdit.setMaximum(1000000)
        self.priceEdit.setDecimals(2)
        self.priceEdit.setValue(0)
        self.formGridLayout.addWidget(self.priceLabel, 1, 2)
        self.formGridLayout.addWidget(self.priceEdit, 1, 3)

        self.unitLabel = QLabel(self.formContainer)
        self.unitLabel.setObjectName(u"unitLabel")
        self.unitEdit = QLineEdit(self.formContainer)
        self.unitEdit.setObjectName(u"unitEdit")
        self.unitEdit.setMinimumHeight(26)
        self.formGridLayout.addWidget(self.unitLabel, 2, 2)
        self.formGridLayout.addWidget(self.unitEdit, 2, 3)

        self.quantityLabel = QLabel(self.formContainer)
        self.quantityLabel.setObjectName(u"quantityLabel")
        self.quantityEdit = QSpinBox(self.formContainer)
        self.quantityEdit.setObjectName(u"quantityEdit")
        self.quantityEdit.setMinimumHeight(26)
        self.quantityEdit.setMinimum(0)
        self.quantityEdit.setMaximum(10000)
        self.quantityEdit.setValue(0)
        self.formGridLayout.addWidget(self.quantityLabel, 3, 2)
        self.formGridLayout.addWidget(self.quantityEdit, 3, 3)

        self.discountLabel = QLabel(self.formContainer)
        self.discountLabel.setObjectName(u"discountLabel")
        self.discountEdit = QDoubleSpinBox(self.formContainer)
        self.discountEdit.setObjectName(u"discountEdit")
        self.discountEdit.setMinimumHeight(26)
        self.discountEdit.setMinimum(0)
        self.discountEdit.setMaximum(100)
        self.discountEdit.setDecimals(2)
        self.discountEdit.setValue(0)
        self.formGridLayout.addWidget(self.discountLabel, 4, 2)
        self.formGridLayout.addWidget(self.discountEdit, 4, 3)

    def setStyleSheet(self, ProductEditWindow):
        ProductEditWindow.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Times New Roman';
            }
            QLabel {
                color: black;
                font-size: 13px;
                font-weight: bold;
                padding: 3px 0;
            }
            QPushButton {
                color: black;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
            /* Основные настройки для полей ввода */
            QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox {
                border: 1px solid #C2C7CB;
                border-radius: 3px;
                padding: 4px 8px;
                background-color: white;
                min-height: 26px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #7FFF00;
                background-color: #F8FFF8;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #C2C7CB;
                border-radius: 3px;
                background-color: white;
                outline: none;
                font-size: 13px;
            }
            QComboBox QAbstractItemView::item {
                padding: 4px 8px;
                border: none;
                outline: none;
                background-color: transparent;
            }
            QComboBox QAbstractItemView::item:selected:active {
                border-left: 2px solid #7FFF00;
                background-color: transparent;
                color: black;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F0F0F0;
                color: black;
            }
            /* ТОЛЬКО размеры для элементов управления, внешний вид - стандартный */
            QComboBox::drop-down {
                width: 20px;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                selection-background-color: #7FFF00;
                selection-color: black;
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

        self.headerLabel.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: black;
                padding: 8px;
                margin-bottom: 5px;
                border-bottom: 1px solid #7FFF00;
            }
        """)

        self.imageLabel.setStyleSheet("""
            border: 1px solid #ccc;
            background-color: white;
            color: black;
            font-weight: bold;
            font-size: 13px;
        """)

        self.loadImageBtn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
            QPushButton:pressed {
                background-color: #5EDF00;
            }
        """)

        self.clearImageBtn.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
            QPushButton:pressed {
                background-color: #00D67A;
            }
        """)

        self.saveBtn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
            QPushButton:pressed {
                background-color: #5EDF00;
            }
        """)

        self.cancelBtn.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
            QPushButton:pressed {
                background-color: #00D67A;
            }
        """)

    def retranslateUi(self, ProductEditWindow):
        ProductEditWindow.setWindowTitle(
            QCoreApplication.translate("ProductEditWindow", u"Редактирование товара", None))
        self.headerLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Редактирование товара", None))
        self.nameLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Наименование:", None))
        self.categoryLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Категория:", None))
        self.descriptionLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Описание:", None))
        self.manufacturerLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Производитель:", None))
        self.providerLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Поставщик:", None))
        self.priceLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Цена:", None))
        self.unitLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Единица измерения:", None))
        self.quantityLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Количество на складе:", None))
        self.discountLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Скидка (%):", None))
        self.imageLabel.setText(QCoreApplication.translate("ProductEditWindow", u"Изображение не выбрано", None))
        self.loadImageBtn.setText(QCoreApplication.translate("ProductEditWindow", u"Загрузить изображение", None))
        self.clearImageBtn.setText(QCoreApplication.translate("ProductEditWindow", u"Очистить", None))
        self.saveBtn.setText(QCoreApplication.translate("ProductEditWindow", u"Сохранить", None))
        self.cancelBtn.setText(QCoreApplication.translate("ProductEditWindow", u"Отмена", None))