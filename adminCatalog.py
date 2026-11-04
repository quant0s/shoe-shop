from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget, QFrame,
                               QSpacerItem, QSizePolicy)


class Ui_AdminCatalogWindow(object):
    def setupUi(self, AdminCatalogWindow):
        if not AdminCatalogWindow.objectName():
            AdminCatalogWindow.setObjectName(u"AdminCatalogWindow")
        AdminCatalogWindow.resize(1200, 800)  # Размер как в менеджере

        self.verticalLayout = QVBoxLayout(AdminCatalogWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        self.headerContainer = QFrame(AdminCatalogWindow)
        self.headerContainer.setObjectName(u"headerContainer")
        self.headerContainer.setFixedHeight(80)  # Высота как в менеджере
        self.headerContainer.setStyleSheet(u"background-color: #7FFF00;")  # Цвет как в менеджере

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

        self.headerLayout.addStretch()

        self.rightContainer = QWidget(self.headerContainer)
        self.rightContainer.setObjectName(u"rightContainer")
        self.rightContainer.setMinimumSize(QSize(350, 0))
        self.rightLayout = QHBoxLayout(self.rightContainer)
        self.rightLayout.setSpacing(10)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 0, 0)

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
        self.userInfoLabel.setStyleSheet("")

        self.rightLayout.addWidget(self.userInfoLabel, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.headerLayout.addWidget(self.rightContainer, 0, Qt.AlignmentFlag.AlignRight)

        self.verticalLayout.addWidget(self.headerContainer)

        self.mainContainer = QWidget(AdminCatalogWindow)
        self.mainContainer.setObjectName(u"mainContainer")
        self.mainContainer.setStyleSheet(u"background-color: white;")

        self.mainContainerLayout = QVBoxLayout(self.mainContainer)
        self.mainContainerLayout.setObjectName(u"mainContainerLayout")
        self.mainContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.mainContainerLayout.setSpacing(0)

        self.tabWidget = QTabWidget(self.mainContainer)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"""
            QTabWidget::pane {
                border: 1px solid #C2C7CB;
                background-color: white;
                top: -1px;
                position: absolute;
            }

            QTabWidget::tab-bar {
                alignment: left;
            }

            QTabBar::tab {
                background-color: white;
                border: 1px solid #C2C7CB;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 100px;
                padding: 10px 20px;
                margin-right: 2px;
                margin-bottom: -1px;
                font-size: 14px;
                font-weight: bold;
            }

            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #7FFF00;
                font-weight: bold;
            }

            QTabBar::tab:!selected {
                margin-top: 2px;
                background-color: #F0F0F0;
            }

            QTabBar::tab:hover {
                background-color: #E8E8E8;
            }

            QLineEdit#productsSearch {
                border: 1px solid #C2C7CB;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                font-size: 14px;
            }

            QLineEdit#productsSearch:focus {
                border: 2px solid #7FFF00;
                background-color: #F8FFF8;
            }

            QComboBox {
                border: 1px solid #C2C7CB;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                min-width: 140px;
                font-size: 14px;
            }

            QComboBox:focus {
                border: 2px solid #7FFF00;
                background-color: #F8FFF8;
            }

            QComboBox QAbstractItemView {
                border: 1px solid #C2C7CB;
                border-radius: 4px;
                background-color: white;
                outline: none;
                font-size: 14px;
            }

            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
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

            QComboBox::drop-down {
                border: none;
                width: 20px;
            }

            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)

        self.productsTab = QWidget()
        self.productsTab.setObjectName(u"productsTab")
        self.productsTabLayout = QVBoxLayout(self.productsTab)
        self.productsTabLayout.setObjectName(u"productsTabLayout")
        self.productsTabLayout.setContentsMargins(0, 0, 0, 0)
        self.productsTabLayout.setSpacing(0)

        self.productsControlsContainer = QWidget(self.productsTab)
        self.productsControlsContainer.setObjectName(u"productsControlsContainer")
        self.productsControlsContainer.setStyleSheet(u"""
            background-color: white; 
            border-bottom: 1px solid #C2C7CB;
            padding-top: 5px;
        """)
        self.productsControlsContainer.setMinimumHeight(60)

        self.productsControlsLayout = QHBoxLayout(self.productsControlsContainer)
        self.productsControlsLayout.setObjectName(u"productsControlsLayout")
        self.productsControlsLayout.setContentsMargins(20, 10, 20, 10)
        self.productsControlsLayout.setSpacing(15)

        self.productsSearch = QLineEdit(self.productsControlsContainer)
        self.productsSearch.setObjectName(u"productsSearch")
        self.productsSearch.setFixedHeight(32)
        self.productsSearch.setStyleSheet("font-size: 14px;")
        self.productsControlsLayout.addWidget(self.productsSearch)

        self.productsSort = QComboBox(self.productsControlsContainer)
        self.productsSort.addItem("")
        self.productsSort.addItem("")
        self.productsSort.addItem("")
        self.productsSort.setObjectName(u"productsSort")
        self.productsSort.setFixedHeight(32)
        self.productsSort.setStyleSheet("font-size: 14px;")
        self.productsControlsLayout.addWidget(self.productsSort)

        self.productsFilter = QComboBox(self.productsControlsContainer)
        self.productsFilter.addItem("")
        self.productsFilter.setObjectName(u"productsFilter")
        self.productsFilter.setFixedHeight(32)
        self.productsFilter.setStyleSheet("font-size: 14px;")
        self.productsControlsLayout.addWidget(self.productsFilter)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.productsControlsLayout.addItem(spacer)

        self.addProductBtn = QPushButton(self.productsControlsContainer)
        self.addProductBtn.setObjectName(u"addProductBtn")
        self.addProductBtn.setFixedHeight(32)
        self.addProductBtn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: black;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
            QPushButton:pressed {
                background-color: #5EDF00;
            }
        """)
        self.productsControlsLayout.addWidget(self.addProductBtn)

        self.deleteProductBtn = QPushButton(self.productsControlsContainer)
        self.deleteProductBtn.setObjectName(u"deleteProductBtn")
        self.deleteProductBtn.setFixedHeight(32)
        self.deleteProductBtn.setVisible(False)
        self.deleteProductBtn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: black;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
            QPushButton:pressed {
                background-color: #5EDF00;
            }
        """)
        self.productsControlsLayout.addWidget(self.deleteProductBtn)

        self.productsTabLayout.addWidget(self.productsControlsContainer)

        self.productsScrollArea = QScrollArea(self.productsTab)
        self.productsScrollArea.setObjectName(u"productsScrollArea")
        self.productsScrollArea.setWidgetResizable(True)
        self.productsScrollArea.setStyleSheet(u"""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #00FA9A;
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

        self.productsScrollAreaWidgetContents = QWidget()
        self.productsScrollAreaWidgetContents.setObjectName(u"productsScrollAreaWidgetContents")
        self.productsScrollAreaWidgetContents.setGeometry(QRect(0, 0, 1176, 690))
        self.productsScrollAreaWidgetContents.setStyleSheet("background-color: white;")

        self.productsLayout = QVBoxLayout(self.productsScrollAreaWidgetContents)
        self.productsLayout.setObjectName(u"productsLayout")
        self.productsLayout.setSpacing(12)
        self.productsLayout.setContentsMargins(20, 20, 20, 20)

        self.productsScrollArea.setWidget(self.productsScrollAreaWidgetContents)
        self.productsTabLayout.addWidget(self.productsScrollArea)

        self.tabWidget.addTab(self.productsTab, "")

        self.ordersTab = QWidget()
        self.ordersTab.setObjectName(u"ordersTab")
        self.ordersTabLayout = QVBoxLayout(self.ordersTab)
        self.ordersTabLayout.setObjectName(u"ordersTabLayout")
        self.ordersTabLayout.setContentsMargins(0, 0, 0, 0)
        self.ordersTabLayout.setSpacing(0)

        self.ordersControlsContainer = QWidget(self.ordersTab)
        self.ordersControlsContainer.setObjectName(u"ordersControlsContainer")
        self.ordersControlsContainer.setStyleSheet(u"""
            background-color: white; 
            border-bottom: 1px solid #C2C7CB;
            padding-top: 5px;
        """)
        self.ordersControlsContainer.setMinimumHeight(60)

        self.ordersControlsLayout = QHBoxLayout(self.ordersControlsContainer)
        self.ordersControlsLayout.setObjectName(u"ordersControlsLayout")
        self.ordersControlsLayout.setContentsMargins(20, 10, 20, 10)
        self.ordersControlsLayout.setSpacing(15)

        spacer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.ordersControlsLayout.addItem(spacer2)

        self.addOrderBtn = QPushButton(self.ordersControlsContainer)
        self.addOrderBtn.setObjectName(u"addOrderBtn")
        self.addOrderBtn.setFixedHeight(32)
        self.addOrderBtn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: black;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
            QPushButton:pressed {
                background-color: #5EDF00;
            }
        """)
        self.ordersControlsLayout.addWidget(self.addOrderBtn)

        self.testOrdersBtn = QPushButton(self.ordersControlsContainer)
        self.testOrdersBtn.setObjectName(u"testOrdersBtn")
        self.testOrdersBtn.setFixedHeight(32)
        self.testOrdersBtn.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
                color: black;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
            QPushButton:pressed {
                background-color: #00D67A;
            }
        """)
        self.ordersControlsLayout.addWidget(self.testOrdersBtn)

        self.ordersTabLayout.addWidget(self.ordersControlsContainer)

        self.ordersScrollArea = QScrollArea(self.ordersTab)
        self.ordersScrollArea.setObjectName(u"ordersScrollArea")
        self.ordersScrollArea.setWidgetResizable(True)
        self.ordersScrollArea.setStyleSheet(u"""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #00FA9A;
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

        self.ordersScrollAreaWidgetContents = QWidget()
        self.ordersScrollAreaWidgetContents.setObjectName(u"ordersScrollAreaWidgetContents")
        self.ordersScrollAreaWidgetContents.setGeometry(QRect(0, 0, 1176, 690))
        self.ordersScrollAreaWidgetContents.setStyleSheet("background-color: white;")

        self.ordersLayout = QVBoxLayout(self.ordersScrollAreaWidgetContents)
        self.ordersLayout.setObjectName(u"ordersLayout")
        self.ordersLayout.setSpacing(12)
        self.ordersLayout.setContentsMargins(20, 20, 20, 20)

        self.ordersScrollArea.setWidget(self.ordersScrollAreaWidgetContents)
        self.ordersTabLayout.addWidget(self.ordersScrollArea)

        self.tabWidget.addTab(self.ordersTab, "")

        self.mainContainerLayout.addSpacing(5)
        self.mainContainerLayout.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.mainContainer)

        self.retranslateUi(AdminCatalogWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(AdminCatalogWindow)

    def retranslateUi(self, AdminCatalogWindow):
        AdminCatalogWindow.setWindowTitle(
            QCoreApplication.translate("AdminCatalogWindow", u"Каталог товаров (Администратор)", None))
        self.logoLabel.setText(
            QCoreApplication.translate("AdminCatalogWindow", u"\u041b\u041e\u0413\u041e\u0422\u0418\u041f", None))
        self.titleLabel.setText(QCoreApplication.translate("AdminCatalogWindow",
                                                           u"\u041a\u0430\u0442\u0430\u043b\u043e\u0433 \u0442\u043e\u0432\u0430\u0440\u043e\u0432",
                                                           None))
        self.logoutBtn.setText(
            QCoreApplication.translate("AdminCatalogWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.userInfoLabel.setText(
            QCoreApplication.translate("AdminCatalogWindow",
                                       u"\u0410\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440",
                                       None))
        self.productsSearch.setPlaceholderText(QCoreApplication.translate("AdminCatalogWindow",
                                                                          u"\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e, \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438, \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044e...",
                                                                          None))
        self.productsSort.setItemText(0, QCoreApplication.translate("AdminCatalogWindow",
                                                                    u"\u0421\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0430 \u043f\u043e \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0443",
                                                                    None))
        self.productsSort.setItemText(1, QCoreApplication.translate("AdminCatalogWindow",
                                                                    u"\u041f\u043e \u0432\u043e\u0437\u0440\u0430\u0441\u0442\u0430\u043d\u0438\u044e",
                                                                    None))
        self.productsSort.setItemText(2, QCoreApplication.translate("AdminCatalogWindow",
                                                                    u"\u041f\u043e \u0443\u0431\u044b\u0432\u0430\u043d\u0438\u044e",
                                                                    None))

        self.productsFilter.setItemText(0, QCoreApplication.translate("AdminCatalogWindow",
                                                                      u"\u0412\u0441\u0435 \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0438",
                                                                      None))

        self.addProductBtn.setText(
            QCoreApplication.translate("AdminCatalogWindow",
                                       u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u043e\u0432\u0430\u0440",
                                       None))
        self.deleteProductBtn.setText(
            QCoreApplication.translate("AdminCatalogWindow", u"Удалить", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.productsTab),
                                  QCoreApplication.translate("AdminCatalogWindow",
                                                             u"\u0422\u043e\u0432\u0430\u0440\u044b", None))
        self.addOrderBtn.setText(
            QCoreApplication.translate("AdminCatalogWindow",
                                       u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u043a\u0430\u0437",
                                       None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ordersTab),
                                  QCoreApplication.translate("AdminCatalogWindow",
                                                             u"\u0417\u0430\u043a\u0430\u0437\u044b", None))
        self.testOrdersBtn.setText(
            QCoreApplication.translate(
                "AdminCatalogWindow",
                u"Тестирование заказов",
                None
            )
        )
