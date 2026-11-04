from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel,
                               QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
                               QVBoxLayout, QWidget)


class Ui_GuestCatalogWindow(object):
    def setupUi(self, CatalogWindow):
        if not CatalogWindow.objectName():
            CatalogWindow.setObjectName(u"GuestCatalogWindow")
        CatalogWindow.resize(850, 600)
        self.productTemplateWidget = QWidget(CatalogWindow)
        self.productTemplateWidget.setObjectName(u"productTemplateWidget")
        self.productTemplateWidget.setGeometry(QRect(100, 100, 600, 140))
        self.productTemplateWidget.setMinimumSize(QSize(0, 140))
        self.productTemplateWidget.setVisible(False)

        self.headerContainer = QFrame(CatalogWindow)
        self.headerContainer.setObjectName(u"headerContainer")
        self.headerContainer.setFixedHeight(80)
        self.headerContainer.setStyleSheet(u"background-color: #7FFF00;")

        self.productTemplateLayout = QHBoxLayout(self.productTemplateWidget)
        self.productTemplateLayout.setSpacing(15)
        self.productTemplateLayout.setObjectName(u"productTemplateLayout")
        self.productTemplateLayout.setContentsMargins(15, 10, 15, 10)

        self.templatePhotoLabel = QLabel(self.productTemplateWidget)
        self.templatePhotoLabel.setObjectName(u"templatePhotoLabel")
        self.templatePhotoLabel.setMinimumSize(QSize(120, 120))
        self.templatePhotoLabel.setMaximumSize(QSize(120, 120))
        self.templatePhotoLabel.setStyleSheet(u"border: 1px solid #ccc; \n"
                                              "background-color: white;\n"
                                              "font-weight: bold;")
        self.templatePhotoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.productTemplateLayout.addWidget(self.templatePhotoLabel)

        self.templateCenterFrame = QFrame(self.productTemplateWidget)
        self.templateCenterFrame.setObjectName(u"templateCenterFrame")
        self.templateCenterFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.templateCenterLayout = QVBoxLayout(self.templateCenterFrame)
        self.templateCenterLayout.setSpacing(4)
        self.templateCenterLayout.setObjectName(u"templateCenterLayout")
        self.templateCenterLayout.setContentsMargins(8, 0, 8, 0)

        self.templateCategoryNameLabel = QLabel(self.templateCenterFrame)
        self.templateCategoryNameLabel.setObjectName(u"templateCategoryNameLabel")
        self.templateCategoryNameLabel.setStyleSheet(u"font-weight: bold; color: #333333;")

        self.templateCenterLayout.addWidget(self.templateCategoryNameLabel)

        self.templateDescriptionLabel = QLabel(self.templateCenterFrame)
        self.templateDescriptionLabel.setObjectName(u"templateDescriptionLabel")
        self.templateDescriptionLabel.setMaximumSize(QSize(16777215, 40))
        self.templateDescriptionLabel.setWordWrap(True)

        self.templateCenterLayout.addWidget(self.templateDescriptionLabel)

        self.templateManufacturerLabel = QLabel(self.templateCenterFrame)
        self.templateManufacturerLabel.setObjectName(u"templateManufacturerLabel")
        self.templateManufacturerLabel.setStyleSheet(u"color: #555555;")

        self.templateCenterLayout.addWidget(self.templateManufacturerLabel)

        self.templateSupplierLabel = QLabel(self.templateCenterFrame)
        self.templateSupplierLabel.setObjectName(u"templateSupplierLabel")
        self.templateSupplierLabel.setStyleSheet(u"color: #555555;")

        self.templateCenterLayout.addWidget(self.templateSupplierLabel)

        self.templatePriceLabel = QLabel(self.templateCenterFrame)
        self.templatePriceLabel.setObjectName(u"templatePriceLabel")
        self.templatePriceLabel.setStyleSheet(u"color: #222222;")

        self.templateCenterLayout.addWidget(self.templatePriceLabel)

        self.templateQuantityLayout = QHBoxLayout()
        self.templateQuantityLayout.setObjectName(u"templateQuantityLayout")
        self.templateUnitLabel = QLabel(self.templateCenterFrame)
        self.templateUnitLabel.setObjectName(u"templateUnitLabel")
        self.templateUnitLabel.setStyleSheet(u"color: #555555;")

        self.templateQuantityLayout.addWidget(self.templateUnitLabel)

        self.templateQuantityLabel = QLabel(self.templateCenterFrame)
        self.templateQuantityLabel.setObjectName(u"templateQuantityLabel")
        self.templateQuantityLabel.setStyleSheet(u"color: #555555;")

        self.templateQuantityLayout.addWidget(self.templateQuantityLabel)

        self.templateHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.templateQuantityLayout.addItem(self.templateHorizontalSpacer)

        self.templateCenterLayout.addLayout(self.templateQuantityLayout)

        self.productTemplateLayout.addWidget(self.templateCenterFrame)

        self.templateDiscountLayout = QVBoxLayout()
        self.templateDiscountLayout.setSpacing(5)
        self.templateDiscountLayout.setObjectName(u"templateDiscountLayout")
        self.templateDiscountLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.templateDiscountTitleLabel = QLabel(self.productTemplateWidget)
        self.templateDiscountTitleLabel.setObjectName(u"templateDiscountTitleLabel")
        self.templateDiscountTitleLabel.setMinimumSize(QSize(100, 30))
        self.templateDiscountTitleLabel.setStyleSheet(u"font-weight: bold; color: #333333;")
        self.templateDiscountTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.templateDiscountLayout.addWidget(self.templateDiscountTitleLabel)

        self.templateDiscountValueLabel = QLabel(self.productTemplateWidget)
        self.templateDiscountValueLabel.setObjectName(u"templateDiscountValueLabel")
        self.templateDiscountValueLabel.setMinimumSize(QSize(80, 40))
        self.templateDiscountValueLabel.setStyleSheet(u"font-weight: bold; color: #7FFF00; font-size: 16px;")
        self.templateDiscountValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.templateDiscountLayout.addWidget(self.templateDiscountValueLabel)

        self.productTemplateLayout.addLayout(self.templateDiscountLayout)

        self.mainLayout = QVBoxLayout(CatalogWindow)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.headerLayout = QHBoxLayout(self.headerContainer)
        self.headerLayout.setSpacing(0)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(0, 0, 0, 0)

        self.logoLabel = QLabel(self.headerContainer)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setMinimumSize(QSize(80, 80))
        self.logoLabel.setMaximumSize(QSize(80, 80))
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerLayout.addWidget(self.logoLabel)

        self.titleLabel = QLabel(self.headerContainer)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(12)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerLayout.addWidget(self.titleLabel)

        self.rightContainer = QWidget(self.headerContainer)
        self.rightContainer.setObjectName(u"rightContainer")
        self.rightContainer.setMinimumSize(QSize(350, 0))
        self.rightLayout = QHBoxLayout(self.rightContainer)
        self.rightLayout.setSpacing(10)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 20, 0)

        self.logoutBtn = QPushButton(self.rightContainer)
        self.logoutBtn.setObjectName(u"logoutBtn")
        self.logoutBtn.setMinimumSize(QSize(87, 0))
        self.logoutBtn.setMaximumSize(QSize(87, 16777215))
        self.logoutBtn.setStyleSheet(u"""
            QPushButton {
                background-color: #00FA9A;
                color: black;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
            QPushButton:pressed {
                background-color: #00D67A;
            }
        """)
        self.logoutBtn.setFont(font)
        self.logoutBtn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.rightLayout.addWidget(self.logoutBtn)

        self.userInfoLabel = QLabel(self.rightContainer)
        self.userInfoLabel.setObjectName(u"userInfoLabel")
        self.userInfoLabel.setEnabled(True)
        self.userInfoLabel.setMinimumSize(QSize(250, 30))
        self.userInfoLabel.setMaximumSize(QSize(250, 30))
        self.userInfoLabel.setFont(font)
        self.userInfoLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.userInfoLabel.setLineWidth(4)
        self.userInfoLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.userInfoLabel.setIndent(0)

        self.rightLayout.addWidget(self.userInfoLabel, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.rightLayout.addStretch()
        self.headerLayout.addWidget(self.rightContainer, 0, Qt.AlignmentFlag.AlignRight)

        self.mainLayout.addWidget(self.headerContainer)

        self.scrollArea = QScrollArea(CatalogWindow)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet(u"""
            QScrollArea {
                border: none;
                background-color: #00FA9A;  /* Ближе к нужному цвету */
                border-top: 1px solid #00E68A;
            }
            QScrollBar:vertical {
                background-color: #00FA9A;  /* Цвет как в оригинале */
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #7FFF00;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6FE600;
            }
        """)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 830, 520))
        self.scrollAreaWidgetContents.setStyleSheet(
            "background-color: white; border: 1px solid #00E68A;")  # Добавил границу

        self.productsLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.productsLayout.setObjectName(u"productsLayout")
        self.productsLayout.setSpacing(12)
        self.productsLayout.setContentsMargins(20, 20, 20, 20)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.mainLayout.addWidget(self.scrollArea)

        self.retranslateUi(CatalogWindow)

        QMetaObject.connectSlotsByName(CatalogWindow)

    def retranslateUi(self, GuestCatalogWindow):
        GuestCatalogWindow.setWindowTitle(QCoreApplication.translate("CatalogWindow", u"Каталог товаров", None))
        self.templatePhotoLabel.setText(QCoreApplication.translate("CatalogWindow", u"Фото", None))
        self.templateCategoryNameLabel.setText(
            QCoreApplication.translate("CatalogWindow", u"Категория | Наименование", None))
        self.templateDescriptionLabel.setText(
            QCoreApplication.translate("CatalogWindow", u"Описание товара: Описание товара будет здесь", None))
        self.templateManufacturerLabel.setText(
            QCoreApplication.translate("CatalogWindow", u"Производитель: Производитель", None))
        self.templateSupplierLabel.setText(QCoreApplication.translate("CatalogWindow", u"Поставщик: Поставщик", None))
        self.templatePriceLabel.setText(QCoreApplication.translate("CatalogWindow", u"Цена: 0.00 ₽", None))
        self.templateUnitLabel.setText(QCoreApplication.translate("CatalogWindow", u"Единица измерения: шт", None))
        self.templateQuantityLabel.setText(
            QCoreApplication.translate("CatalogWindow", u"Количество на складе: 0", None))
        self.templateDiscountTitleLabel.setText(
            QCoreApplication.translate("CatalogWindow", u"Действующая\nскидка", None))
        self.templateDiscountValueLabel.setText(QCoreApplication.translate("CatalogWindow", u"0%", None))
        self.logoLabel.setText(QCoreApplication.translate("CatalogWindow", u"ЛОГОТИП", None))
        self.titleLabel.setText(QCoreApplication.translate("CatalogWindow", u"Каталог товаров", None))
        self.logoutBtn.setText(QCoreApplication.translate("CatalogWindow", u"Выход", None))
        self.userInfoLabel.setText(QCoreApplication.translate("CatalogWindow", u"Гость", None))