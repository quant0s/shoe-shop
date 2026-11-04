from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout)


class Ui_LoginWindow(object):
    def setupUi(self, LoginWidget):
        if not LoginWidget.objectName():
            LoginWidget.setObjectName(u"LoginWidget")
        LoginWidget.resize(500, 400)

        main_widget = QWidget(LoginWidget)
        main_widget.setObjectName(u"main_widget")

        main_layout = QVBoxLayout(main_widget)
        main_layout.setObjectName(u"main_layout")
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(25)

        main_layout.addStretch(1)

        title_font = QFont()
        title_font.setFamilies([u"Times New Roman"])
        title_font.setPointSize(26)
        title_font.setBold(True)
        title_font.setWeight(QFont.Bold)

        main_font = QFont()
        main_font.setFamilies([u"Times New Roman"])
        main_font.setPointSize(12)

        self.name_window = QLabel(main_widget)
        self.name_window.setObjectName(u"name_window")
        self.name_window.setFont(title_font)
        self.name_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.name_window)

        main_layout.addSpacing(40)

        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(20)

        login_layout = QVBoxLayout()
        self.text_login = QLabel(main_widget)
        self.text_login.setObjectName(u"text_login")
        self.text_login.setFont(main_font)
        login_layout.addWidget(self.text_login)

        self.username_input = QLineEdit(main_widget)
        self.username_input.setObjectName(u"username_input")
        self.username_input.setFont(main_font)
        self.username_input.setMinimumHeight(40)
        login_layout.addWidget(self.username_input)

        password_layout = QVBoxLayout()
        self.text_password = QLabel(main_widget)
        self.text_password.setObjectName(u"text_password")
        self.text_password.setFont(main_font)
        password_layout.addWidget(self.text_password)

        self.password_input = QLineEdit(main_widget)
        self.password_input.setObjectName(u"password_input")
        self.password_input.setFont(main_font)
        self.password_input.setMinimumHeight(40)
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)

        fields_layout.addLayout(login_layout)
        fields_layout.addLayout(password_layout)
        main_layout.addLayout(fields_layout)

        main_layout.addSpacing(25)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.login_btn = QPushButton(main_widget)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setFont(main_font)
        self.login_btn.setMinimumHeight(45)
        buttons_layout.addWidget(self.login_btn)

        self.guest_btn = QPushButton(main_widget)
        self.guest_btn.setObjectName(u"guest_btn")
        self.guest_btn.setFont(main_font)
        self.guest_btn.setMinimumHeight(45)
        buttons_layout.addWidget(self.guest_btn)

        main_layout.addLayout(buttons_layout)

        main_layout.addStretch(1)

        LoginWidget.setLayout(main_layout)

        self.setStyleSheet(LoginWidget)

        self.retranslateUi(LoginWidget)
        QMetaObject.connectSlotsByName(LoginWidget)

    def setStyleSheet(self, LoginWidget):
        LoginWidget.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Times New Roman';
            }
            QLabel, QLineEdit, QPushButton {
                color: #333333;
            }
            QPushButton#login_btn, 
            QPushButton#guest_btn {
                background-color: #7FFF00;
                color: #333333;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                font-size: 15px;
                min-width: 160px;
            }
            QPushButton#login_btn:hover, 
            QPushButton#guest_btn:hover {
                background-color: #6FE600;
                box-shadow: 0px 3px 6px rgba(127, 255, 0, 0.2);
            }
            QPushButton#login_btn:pressed, 
            QPushButton#guest_btn:pressed {
                background-color: #5FCC00;
                box-shadow: 0px 1px 3px rgba(127, 255, 0, 0.3);
            }
            QLineEdit {
                border: 2px solid #D0D0D0;
                border-radius: 6px;
                background-color: white;
                padding: 10px 15px;
                color: #333333;
                selection-background-color: #7FFF00;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #7FFF00;
                background-color: #FAFFFA;
                box-shadow: 0px 0px 4px rgba(127, 255, 0, 0.2);
            }
            QLineEdit::placeholder {
                color: #888888;
            }
            QLabel#name_window {
                color: #222222;
                padding-bottom: 5px;
            }
        """)

    def retranslateUi(self, LoginWidget):
        LoginWidget.setWindowTitle(QCoreApplication.translate("LoginWidget", u"Авторизация", None))
        self.name_window.setText(QCoreApplication.translate("LoginWidget", u"Авторизация", None))
        self.login_btn.setText(QCoreApplication.translate("LoginWidget", u"Войти", None))
        self.text_login.setText(QCoreApplication.translate("LoginWidget", u"Логин", None))
        self.text_password.setText(QCoreApplication.translate("LoginWidget", u"Пароль", None))
        self.guest_btn.setText(QCoreApplication.translate("LoginWidget", u"Войти как гость", None))
        self.username_input.setPlaceholderText(QCoreApplication.translate("LoginWidget", u"Введите ваш рабочий логин", None))
        self.password_input.setPlaceholderText(QCoreApplication.translate("LoginWidget", u"Введите пароль", None))