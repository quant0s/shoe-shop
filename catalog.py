import os
import sys
import random

os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=0'
os.environ['QT_STYLE_OVERRIDE'] = ''

from datetime import datetime
import psycopg
from PIL import Image
from PySide6.QtCore import Qt, Signal, QDate, QTimer
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QPushButton, QStackedWidget, QMessageBox,
                               QHBoxLayout, QFrame, QSizePolicy, QFileDialog, QDialog)

from adminCatalog import Ui_AdminCatalogWindow
from clientCatalog import Ui_ClientCatalogWindow
from guestCatalog import Ui_GuestCatalogWindow
from loginWindow import Ui_LoginWindow
from managerCatalog import Ui_ManagerCatalogWindow
from productEditWindow import Ui_ProductEditWindow
from orderEditWindow import Ui_OrderEditWindow
from product_selection_window import ProductSelectionWindow

import configparser

def get_db_connection():
    """Получение подключения к БД PostgreSQL из конфигурационного файла config.ini."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    if not os.path.exists(config_path):
        config_path = "config.ini"
    config.read(config_path, encoding="utf-8")
    if "database" in config:
        db = config["database"]
        return psycopg.connect(
            host=db.get("host", "localhost"),
            port=db.get("port", "5432"),
            dbname=db.get("name", "shoe_shop"),
            user=db.get("user", "postgres"),
            password=db.get("password", "")
        )
    raise RuntimeError("Файл конфигурации config.ini не найден или повреждён. Создайте его на основе config.ini.example.")


if sys.platform == "win32":
    QApplication.setStyle("Windows")


class ProductEditWindow(QWidget):
    product_saved = Signal()
    closed = Signal()

    def __init__(self, mode='add', product_id=None, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.product_id = product_id
        self.parent = parent
        self.image_path = None
        self.original_image_path = None
        self.image_cleared = False

        self.ui = Ui_ProductEditWindow()
        self.ui.setupUi(self)

        title = "Добавление товара" if mode == 'add' else "Редактирование товара"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("import/Icon.png"))
        self.setMinimumSize(550, 700)

        self.ui.headerLabel.setText(title)

        self.setup_connections()

        self.load_categories()
        self.load_manufacturers()

        if mode == 'edit' and product_id:
            self.load_product_data()
        elif mode == 'add':
            self.set_default_image()

    def setup_connections(self):
        self.ui.loadImageBtn.clicked.connect(self.load_image)
        self.ui.clearImageBtn.clicked.connect(self.clear_image)
        self.ui.saveBtn.clicked.connect(self.save_product)
        self.ui.cancelBtn.clicked.connect(self.close)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent:
            parent_rect = self.parent.geometry()
            my_rect = self.geometry()
            x = parent_rect.center().x() - my_rect.width() // 2
            y = parent_rect.center().y() - my_rect.height() // 2
            self.move(x, y)

    def set_default_image(self):
        try:
            default_pixmap = QPixmap("import/picture.png")
            if not default_pixmap.isNull():
                scaled_pixmap = default_pixmap.scaled(
                    300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.ui.imageLabel.setPixmap(scaled_pixmap)
                self.ui.imageLabel.setText("")
            else:
                self.ui.imageLabel.setText("Изображение по умолчанию")
        except:
            self.ui.imageLabel.setText("Нет фото")

    def load_categories(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT item_category FROM items WHERE item_category IS NOT NULL ORDER BY item_category"
            )
            categories = cursor.fetchall()
            self.ui.categoryCombo.clear()
            self.ui.categoryCombo.addItem("")
            for category in categories:
                self.ui.categoryCombo.addItem(category[0])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки категорий: {str(e)}")

    def load_manufacturers(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT manufacturer FROM items WHERE manufacturer IS NOT NULL ORDER BY manufacturer"
            )
            manufacturers = cursor.fetchall()
            self.ui.manufacturerCombo.clear()
            self.ui.manufacturerCombo.addItem("")
            for manufacturer in manufacturers:
                self.ui.manufacturerCombo.addItem(manufacturer[0])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки производителей: {str(e)}")

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            try:
                self.image_path = file_path
                self.image_cleared = False
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
                    return

                scaled_pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.ui.imageLabel.setPixmap(scaled_pixmap)
                self.ui.imageLabel.setText("")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки изображения: {str(e)}")

    def clear_image(self):
        self.image_path = None
        self.image_cleared = True
        self.set_default_image()

    def load_product_data(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT name,
                                  item_category,
                                  description,
                                  manufacturer,
                                  provider,
                                  cost,
                                  unit_measurement,
                                  quantity_stock,
                                  current_discount,
                                  photo
                           FROM items
                           WHERE item_number = %s
                           """, (self.product_id,))
            product = cursor.fetchone()
            cursor.close()
            conn.close()

            if product:
                self.ui.nameEdit.setText(str(product[0]) if product[0] else "")

                category_index = self.ui.categoryCombo.findText(str(product[1]) if product[1] else "")
                if category_index >= 0:
                    self.ui.categoryCombo.setCurrentIndex(category_index)

                self.ui.descriptionEdit.setText(str(product[2]) if product[2] else "")

                manufacturer_index = self.ui.manufacturerCombo.findText(str(product[3]) if product[3] else "")
                if manufacturer_index >= 0:
                    self.ui.manufacturerCombo.setCurrentIndex(manufacturer_index)

                self.ui.providerEdit.setText(str(product[4]) if product[4] else "")
                self.ui.priceEdit.setValue(float(product[5]) if product[5] else 0.0)
                self.ui.unitEdit.setText(str(product[6]) if product[6] else "")
                self.ui.quantityEdit.setValue(int(product[7]) if product[7] else 0)
                self.ui.discountEdit.setValue(float(product[8]) if product[8] else 0.0)

                self.original_image_path = str(product[9]) if product[9] else None

                if self.original_image_path and self.original_image_path != 'picture.png':
                    try:
                        photo_path = os.path.join("import", self.original_image_path)
                        if os.path.exists(photo_path):
                            product_pixmap = QPixmap(photo_path)
                            if not product_pixmap.isNull():
                                scaled_pixmap = product_pixmap.scaled(
                                    300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                                )
                                self.ui.imageLabel.setPixmap(scaled_pixmap)
                                self.ui.imageLabel.setText("")
                            else:
                                self.set_default_image()
                        else:
                            self.set_default_image()
                    except:
                        self.set_default_image()
                else:
                    self.set_default_image()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных товара: {str(e)}")

    def save_product(self):
        name = self.ui.nameEdit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Наименование товара не может быть пустым")
            return

        category = self.ui.categoryCombo.currentText().strip()
        description = self.ui.descriptionEdit.text().strip()
        manufacturer = self.ui.manufacturerCombo.currentText().strip()
        provider = self.ui.providerEdit.text().strip()
        price = float(self.ui.priceEdit.value()) if self.ui.priceEdit.value() is not None else 0.0
        unit = self.ui.unitEdit.text().strip()
        quantity = int(self.ui.quantityEdit.value()) if self.ui.quantityEdit.value() is not None else 0
        discount = float(self.ui.discountEdit.value()) if self.ui.discountEdit.value() is not None else 0.0

        if price < 0:
            QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной")
            return

        if discount < 0 or discount > 100:
            QMessageBox.warning(self, "Ошибка", "Скидка должна быть в диапазоне от 0 до 100%")
            return

        # Определяем имя файла изображения
        image_filename = None

        # Случай 1: Загружено новое изображение
        if self.image_path:
            try:
                import_dir = "import"
                if not os.path.exists(import_dir):
                    os.makedirs(import_dir)

                ext = os.path.splitext(self.image_path)[1].lower()
                if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                    ext = '.png'

                if self.mode == 'edit' and self.product_id:
                    base_name = str(self.product_id)
                    image_filename = f"{base_name}{ext}"
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_filename = f"temp_{timestamp}{ext}"

                new_path = os.path.join(import_dir, image_filename)
                counter = 1
                while os.path.exists(new_path):
                    if self.mode == 'edit' and self.product_id:
                        image_filename = f"{self.product_id}_{counter}{ext}"
                    else:
                        image_filename = f"temp_{timestamp}_{counter}{ext}"
                    new_path = os.path.join(import_dir, image_filename)
                    counter += 1

                img = Image.open(self.image_path)
                img.thumbnail((300, 200), Image.Resampling.LANCZOS)

                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else img)
                    img = background

                img.save(new_path)

                # Удаляем старое изображение только если оно не picture.png
                if self.mode == 'edit' and self.original_image_path:
                    old_image_path = os.path.join(import_dir, self.original_image_path)
                    if (os.path.exists(old_image_path) and
                            os.path.isfile(old_image_path) and
                            os.path.basename(old_image_path).lower() != 'picture.png' and
                            old_image_path != new_path):
                        try:
                            os.remove(old_image_path)
                        except:
                            pass

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения изображения: {str(e)}")
                return

        # Случай 2: Пользователь нажал "Очистить изображение"
        elif hasattr(self, 'image_cleared') and self.image_cleared:
            image_filename = 'picture.png'
            # Удаляем старое изображение только если оно не picture.png
            if self.mode == 'edit' and self.original_image_path:
                old_image_path = os.path.join("import", self.original_image_path)
                if (os.path.exists(old_image_path) and
                        os.path.isfile(old_image_path) and
                        os.path.basename(old_image_path).lower() != 'picture.png'):
                    try:
                        os.remove(old_image_path)
                    except:
                        pass

        # Случай 3: Редактирование без изменения изображения - сохраняем старое
        elif self.mode == 'edit' and self.original_image_path:
            image_filename = self.original_image_path

        # Случай 4: Добавление товара без изображения
        else:
            image_filename = 'picture.png'

        # Сохранение в БД
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # ВАЖНО: Отключаем автокоммит для контроля транзакции
            conn.autocommit = False

            if self.mode == 'add':
                # ИСПРАВЛЕНИЕ: Получаем максимальное ЧИСЛОВОЕ значение item_number
                cursor.execute("""
                    SELECT COALESCE(MAX(
                        CASE 
                            WHEN item_number ~ '^[0-9]+$' 
                            THEN CAST(item_number AS INTEGER) 
                            ELSE 0 
                        END
                    ), 0) FROM items
                """)
                max_numeric_id = cursor.fetchone()[0]
                new_id = str(max_numeric_id + 1)

                print(f"DEBUG: Максимальный числовой ID: {max_numeric_id}")
                print(f"DEBUG: Новый ID: {new_id}")

                # Переименовываем временный файл если он есть
                if image_filename and image_filename.startswith('temp_'):
                    temp_ext = os.path.splitext(image_filename)[1]
                    if not temp_ext:
                        temp_ext = '.png'

                    final_image_filename = f"{new_id}{temp_ext}"
                    final_path = os.path.join("import", final_image_filename)
                    temp_path = os.path.join("import", image_filename)

                    counter = 1
                    while os.path.exists(final_path):
                        final_image_filename = f"{new_id}_{counter}{temp_ext}"
                        final_path = os.path.join("import", final_image_filename)
                        counter += 1

                    if os.path.exists(temp_path):
                        try:
                            os.rename(temp_path, final_path)
                            image_filename = final_image_filename
                        except Exception as e:
                            print(f"Ошибка переименования файла: {e}")
                            # В случае ошибки оставляем временное имя

                # Вставляем товар в БД
                cursor.execute("""
                    INSERT INTO items (item_number, name, item_category, description, manufacturer,
                                       provider, cost, unit_measurement, quantity_stock,
                                       current_discount, photo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    new_id,
                    name,
                    category if category else None,
                    description if description else None,
                    manufacturer if manufacturer else None,
                    provider if provider else None,
                    price,
                    unit if unit else None,
                    quantity,
                    discount,
                    image_filename if image_filename else 'picture.png'
                ))

                product_id_for_message = new_id

            else:  # Режим редактирования
                # Для редактирования используем существующий ID
                cursor.execute("""
                    UPDATE items
                    SET name = %s,
                        item_category = %s,
                        description = %s,
                        manufacturer = %s,
                        provider = %s,
                        cost = %s,
                        unit_measurement = %s,
                        quantity_stock = %s,
                        current_discount = %s,
                        photo = %s
                    WHERE item_number = %s
                """, (
                    name,
                    category if category else None,
                    description if description else None,
                    manufacturer if manufacturer else None,
                    provider if provider else None,
                    price,
                    unit if unit else None,
                    quantity,
                    discount,
                    image_filename if image_filename else 'picture.png',
                    self.product_id
                ))

                product_id_for_message = self.product_id

            # КОММИТ транзакции
            conn.commit()
            print(f"DEBUG: Товар успешно сохранен, ID: {product_id_for_message}")

            QMessageBox.information(
                self, "Успех",
                f"Товар {product_id_for_message} успешно сохранен"
            )
            self.product_saved.emit()
            self.close()

        except psycopg.IntegrityError as e:
            if conn:
                conn.rollback()
            error_msg = str(e)
            print(f"DEBUG IntegrityError: {error_msg}")

            if "duplicate key" in error_msg.lower():
                QMessageBox.critical(self, "Ошибка",
                                     f"Товар с таким ID уже существует. Попробуйте еще раз.")
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка целостности данных: {error_msg}")

            # Удаляем временный файл если он был создан
            if self.mode == 'add' and image_filename and image_filename.startswith('temp_'):
                try:
                    temp_path = os.path.join("import", image_filename)
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except:
                    pass

        except psycopg.DataError as e:
            if conn:
                conn.rollback()
            error_msg = str(e)
            print(f"DEBUG DataError: {error_msg}")

            if "integer" in error_msg.lower() and "syntax" in error_msg.lower():
                QMessageBox.critical(self, "Ошибка",
                                     "Ошибка в данных товара. Возможно, в базе есть некорректные ID.\n"
                                     "Проверьте, что все item_number в таблице items являются числами.")
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка данных: {error_msg}")

        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = str(e)
            print(f"DEBUG Общая ошибка: {error_msg}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения товара: {error_msg}")

            # Удаляем временный файл если он был создан
            if self.mode == 'add' and image_filename and image_filename.startswith('temp_'):
                try:
                    temp_path = os.path.join("import", image_filename)
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except:
                    pass
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            if hasattr(self, 'image_cleared'):
                self.image_cleared = False


class OrderEditWindow(QWidget):
    order_saved = Signal()
    closed = Signal()

    def __init__(self, mode='add', order_number=None, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.order_number = order_number
        self.parent = parent

        self.ui = Ui_OrderEditWindow()
        self.ui.setupUi(self)

        self.ui.deleteBtn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 4px;
                    border: 1px solid #5FCC00;
                }
                QPushButton:hover {
                    background-color: #6EEF00;
                }
                QPushButton:pressed {
                    background-color: #5EDF00;
                }
            """)

        title = "Добавление заказа" if mode == 'add' else "Редактирование заказа"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("import/Icon.png"))
        self.setMinimumSize(650, 500)  # Увеличили размер для новой кнопки

        self.ui.headerLabel.setText(title)

        # Добавляем кнопку выбора товаров
        self.select_products_btn = QPushButton("Выбрать товары")
        self.select_products_btn.clicked.connect(self.open_product_selection)

        # Вставляем кнопку перед полем articleText
        # Находим индекс articleText в layout
        layout = self.ui.verticalLayout
        article_text_index = -1
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget == self.ui.articleText:
                article_text_index = i
                break

        if article_text_index != -1:
            layout.insertWidget(article_text_index, self.select_products_btn)
        else:
            # Если не нашли, добавляем в конец перед кнопками
            layout.insertWidget(layout.count() - 3, self.select_products_btn)

        # Настройка кнопки в зависимости от режима
        if mode == 'edit':
            self.ui.deleteBtn.setVisible(True)
            self.ui.articleText.setReadOnly(True)
            self.select_products_btn.setText("Изменить товары")
            self.select_products_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                }
            """)
        else:
            self.ui.deleteBtn.setVisible(False)
            self.select_products_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                }
            """)
            # Не генерируем случайные артикулы - пользователь сам выберет товары

        self.setup_connections()
        self.load_pickup_points()

        if mode == 'edit' and order_number:
            self.load_order_data()

    def setup_connections(self):
        self.ui.saveBtn.clicked.connect(self.save_order)
        self.ui.cancelBtn.clicked.connect(self.close)
        self.ui.deleteBtn.clicked.connect(self.delete_order)

    def open_product_selection(self):
        """Открывает окно выбора товаров"""
        from product_selection_window import \
            ProductSelectionWindow  # Импортируем здесь, чтобы избежать циклических импортов

        dialog = ProductSelectionWindow(self)

        # Если редактируем существующий заказ, предзаполняем выбранные товары
        if self.mode == 'edit' and self.ui.articleText.text():
            # Здесь можно передать предзаполненные данные в диалог
            pass

        if dialog.exec():
            selected_items_str = dialog.get_selected_items_string()
            if selected_items_str:
                self.ui.articleText.setText(selected_items_str)
            elif self.mode == 'add':
                # Если в режиме добавления ничего не выбрано, очищаем поле
                self.ui.articleText.clear()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent:
            parent_rect = self.parent.geometry()
            my_rect = self.geometry()
            x = parent_rect.center().x() - my_rect.width() // 2
            y = parent_rect.center().y() - my_rect.height() // 2
            self.move(x, y)

    def load_pickup_points(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, address FROM pickup_points ORDER BY address")
            points = cursor.fetchall()

            self.ui.addressCombo.clear()
            self.ui.addressCombo.addItem("Выберите пункт выдачи", None)  # Пустой элемент

            for point in points:
                self.ui.addressCombo.addItem(point[1], point[0])

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки пунктов выдачи: {str(e)}")

    def load_order_data(self):
        """Загружает данные заказа для редактирования"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Используем текстовый поиск для order_number (может быть не числом)
            cursor.execute("""
                SELECT order_date, delivery_date, order_status, id_pickup_point
                FROM orders
                WHERE order_number::text = %s
            """, (str(self.order_number),))
            order_data = cursor.fetchone()

            if order_data:
                order_date, delivery_date, order_status, pickup_point_id = order_data

                # Загружаем товары заказа
                cursor.execute("""
                    SELECT item_number, quantity
                    FROM orders_items
                    WHERE order_number::text = %s
                """, (str(self.order_number),))
                order_items = cursor.fetchall()

                # Формируем строку артикулов
                article_parts = []
                for item in order_items:
                    item_number, quantity = item
                    article_parts.append(f"{item_number}#{quantity}")

                article_order = ",".join(article_parts)

                # Устанавливаем даты
                if order_date:
                    try:
                        qdate = QDate.fromString(str(order_date), "yyyy-MM-dd")
                        if qdate.isValid():
                            self.ui.orderDateEdit.setDate(qdate)
                    except:
                        pass

                if delivery_date:
                    try:
                        qdate = QDate.fromString(str(delivery_date), "yyyy-MM-dd")
                        if qdate.isValid():
                            self.ui.deliveryDateEdit.setDate(qdate)
                    except:
                        pass

                # Устанавливаем артикулы
                self.ui.articleText.setText(article_order)

                # Устанавливаем статус
                status_index = self.ui.statusCombo.findText(str(order_status))
                if status_index >= 0:
                    self.ui.statusCombo.setCurrentIndex(status_index)

                # Устанавливаем пункт выдачи
                if pickup_point_id:
                    for i in range(self.ui.addressCombo.count()):
                        if self.ui.addressCombo.itemData(i) == pickup_point_id:
                            self.ui.addressCombo.setCurrentIndex(i)
                            break

            else:
                QMessageBox.warning(self, "Ошибка", f"Заказ с номером {self.order_number} не найден")
                self.close()

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных заказа: {str(e)}")
            print(f"DEBUG Ошибка загрузки заказа: {e}")

    @staticmethod
    def parse_articles(articles_str):
        """Парсит строку артикулов формата item1#qty1,item2#qty2"""
        if not articles_str or str(articles_str).strip() == '':
            return []

        articles_str = str(articles_str).strip()

        # Убираем лишние кавычки если есть
        if articles_str.startswith("'") and articles_str.endswith("'"):
            articles_str = articles_str[1:-1]

        articles_data = []
        for item_str in articles_str.split(','):
            item_str = item_str.strip()
            if '#' in item_str:
                item_parts = item_str.split('#')
                if len(item_parts) == 2:
                    article, quantity_str = item_parts
                    try:
                        quantity = int(quantity_str)
                        if quantity > 0:
                            articles_data.append((article.strip(), quantity))
                    except ValueError:
                        continue

        return articles_data

    def save_order(self):
        """Сохраняет заказ в БД"""
        # Получаем данные из формы
        status = self.ui.statusCombo.currentText().strip()
        pickup_point_id = self.ui.addressCombo.currentData()
        order_date = self.ui.orderDateEdit.date().toString("yyyy-MM-dd")
        delivery_date = self.ui.deliveryDateEdit.date().toString("yyyy-MM-dd")
        article_order = self.ui.articleText.text().strip()

        # Парсим артикулы
        articles_data = self.parse_articles(article_order)

        # ВАЛИДАЦИЯ ДАННЫХ
        if not status:
            QMessageBox.warning(self, "Ошибка", "Необходимо указать статус заказа")
            return

        if not pickup_point_id:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать пункт выдачи")
            return

        if not articles_data:
            QMessageBox.warning(self, "Ошибка", "Необходимо выбрать хотя бы один товар")
            return

        # Проверка дат
        order_qdate = self.ui.orderDateEdit.date()
        delivery_qdate = self.ui.deliveryDateEdit.date()

        if not order_qdate.isValid():
            QMessageBox.warning(self, "Ошибка", "Некорректная дата заказа")
            return

        if not delivery_qdate.isValid():
            QMessageBox.warning(self, "Ошибка", "Некорректная дата доставки")
            return

        if delivery_qdate < order_qdate:
            QMessageBox.warning(self, "Ошибка", "Дата доставки не может быть раньше даты заказа")
            return

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # ВАЖНО: Отключаем автокоммит для контроля транзакции
            conn.autocommit = False

            # Проверяем существование пункта выдачи
            cursor.execute("SELECT id FROM pickup_points WHERE id = %s", (pickup_point_id,))
            if cursor.fetchone() is None:
                QMessageBox.warning(self, "Ошибка", "Выбранный пункт выдачи не существует")
                return

            # Проверяем существование товаров и доступность на складе
            for article, quantity in articles_data:
                cursor.execute("""
                    SELECT item_number, name, quantity_stock 
                    FROM items 
                    WHERE item_number = %s
                """, (article,))
                item_data = cursor.fetchone()

                if not item_data:
                    QMessageBox.warning(self, "Ошибка", f"Товар с артикулом {article} не найден")
                    return

                item_id, item_name, stock_quantity = item_data

                # Если редактируем заказ, учитываем текущее количество в заказе
                if self.mode == 'edit':
                    cursor.execute("""
                        SELECT quantity 
                        FROM orders_items 
                        WHERE order_number = %s AND item_number = %s
                    """, (self.order_number, article))
                    existing_qty_result = cursor.fetchone()
                    existing_qty = existing_qty_result[0] if existing_qty_result else 0

                    # Доступное количество = текущий запас + текущее количество в заказе
                    available_qty = stock_quantity + existing_qty
                else:
                    available_qty = stock_quantity

                if quantity > available_qty:
                    QMessageBox.warning(self, "Ошибка",
                                        f"Недостаточно товара '{item_name}'\n"
                                        f"Запрошено: {quantity} шт., доступно: {available_qty} шт.")
                    return

            # СОХРАНЕНИЕ ЗАКАЗА
            if self.mode == 'add':
                # ИСПРАВЛЕНИЕ: Получаем максимальный ЧИСЛОВОЙ номер заказа
                cursor.execute("""
                    SELECT COALESCE(MAX(
                        CASE 
                            WHEN order_number::text ~ '^[0-9]+$' 
                            THEN CAST(order_number AS INTEGER) 
                            ELSE 0 
                        END
                    ), 0) FROM orders
                """)
                max_order_num = cursor.fetchone()[0]
                new_order_number = int(max_order_num) + 1

                print(f"DEBUG: Максимальный номер заказа: {max_order_num}")
                print(f"DEBUG: Новый номер заказа: {new_order_number}")

                # Генерируем код чека
                try:
                    cursor.execute("SELECT COALESCE(MAX(receipt_code), 0) FROM orders")
                    max_receipt = cursor.fetchone()[0]
                    receipt_code = int(max_receipt) + 1
                except:
                    receipt_code = 1

                # Вставляем заказ
                cursor.execute("""
                    INSERT INTO orders (order_number, order_date, delivery_date, 
                                      receipt_code, order_status, id_pickup_point, id_user)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    new_order_number, order_date, delivery_date,
                    receipt_code, status, pickup_point_id, 1  # Временное значение для id_user
                ))

                # Вставляем товары заказа
                for article, quantity in articles_data:
                    cursor.execute("""
                        INSERT INTO orders_items (order_number, item_number, quantity)
                        VALUES (%s, %s, %s)
                    """, (new_order_number, article, quantity))

                    # Обновляем количество на складе
                    cursor.execute("""
                        UPDATE items 
                        SET quantity_stock = quantity_stock - %s
                        WHERE item_number = %s
                    """, (quantity, article))

                saved_order_number = new_order_number

            else:  # Режим редактирования
                try:
                    order_num = int(self.order_number)
                except ValueError:
                    # Если order_number не число, используем как есть
                    order_num = self.order_number

                # Получаем старые товары для восстановления количества
                cursor.execute("""
                    SELECT item_number, quantity 
                    FROM orders_items 
                    WHERE order_number = %s
                """, (order_num,))
                old_items = cursor.fetchall()

                # Восстанавливаем количество на складе для старых товаров
                for old_article, old_quantity in old_items:
                    cursor.execute("""
                        UPDATE items 
                        SET quantity_stock = quantity_stock + %s
                        WHERE item_number = %s
                    """, (old_quantity, old_article))

                # Удаляем старые товары заказа
                cursor.execute("DELETE FROM orders_items WHERE order_number = %s", (order_num,))

                # Обновляем заказ
                cursor.execute("""
                    UPDATE orders
                    SET order_date = %s,
                        delivery_date = %s,
                        order_status = %s,
                        id_pickup_point = %s
                    WHERE order_number = %s
                """, (order_date, delivery_date, status, pickup_point_id, order_num))

                # Вставляем новые товары заказа
                for article, quantity in articles_data:
                    cursor.execute("""
                        INSERT INTO orders_items (order_number, item_number, quantity)
                        VALUES (%s, %s, %s)
                    """, (order_num, article, quantity))

                    # Уменьшаем количество на складе
                    cursor.execute("""
                        UPDATE items 
                        SET quantity_stock = quantity_stock - %s
                        WHERE item_number = %s
                    """, (quantity, article))

                saved_order_number = order_num

            # КОММИТ транзакции
            conn.commit()
            print(f"DEBUG: Заказ успешно сохранен, номер: {saved_order_number}")

            # Сообщение об успехе
            display_order_number = f"ORD-{saved_order_number:06d}"
            QMessageBox.information(
                self,
                "Успех",
                f"Заказ {display_order_number} успешно сохранен\n"
                f"Статус: {status}\n"
                f"Товаров: {len(articles_data)} позиций"
            )

            # Сигнализируем об успешном сохранении
            self.order_saved.emit()
            self.close()

        except psycopg.DataError as e:
            # ОТКАТ при ошибке данных
            if conn:
                conn.rollback()

            error_msg = str(e)
            print(f"DEBUG DataError при сохранении заказа: {error_msg}")

            if "integer" in error_msg.lower() and "syntax" in error_msg.lower():
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Ошибка в данных заказа. Возможно, в базе есть некорректные номера заказов.\n"
                    "Проверьте, что все order_number в таблице orders являются числами.\n\n"
                    "Рекомендуется:\n"
                    "1. Проверить таблицу orders на наличие букв в order_number\n"
                    "2. Использовать команду для очистки: SELECT * FROM orders WHERE order_number::text !~ '^[0-9]+$'"
                )
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка данных: {error_msg}")

        except psycopg.IntegrityError as e:
            # ОТКАТ при ошибке целостности
            if conn:
                conn.rollback()

            error_msg = str(e)
            print(f"DEBUG IntegrityError при сохранении заказа: {error_msg}")

            if "orders_pkey" in error_msg or "unique constraint" in error_msg.lower():
                # Пробуем сгенерировать новый номер заказа
                try:
                    if conn:
                        # Получаем действительно максимальный номер (любой)
                        cursor.execute("""
                            SELECT COALESCE(MAX(
                                CASE 
                                    WHEN order_number::text ~ '^[0-9]+$' 
                                    THEN CAST(order_number AS INTEGER) 
                                    ELSE 0 
                                END
                            ), 0) FROM orders
                        """)
                        max_order = cursor.fetchone()[0]
                        new_order_number = int(max_order) + 10  # Добавляем 10 чтобы быть уверенным

                        # Сохраняем с новым номером
                        if self.mode == 'add':
                            # Обновляем запрос с новым номером
                            cursor.execute("""
                                INSERT INTO orders (order_number, order_date, delivery_date, 
                                                  receipt_code, order_status, id_pickup_point, id_user)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """, (
                                new_order_number, order_date, delivery_date,
                                receipt_code, status, pickup_point_id, 1
                            ))

                            # Вставляем товары заказа
                            for article, quantity in articles_data:
                                cursor.execute("""
                                    INSERT INTO orders_items (order_number, item_number, quantity)
                                    VALUES (%s, %s, %s)
                                """, (new_order_number, article, quantity))

                                # Обновляем количество на складе
                                cursor.execute("""
                                    UPDATE items 
                                    SET quantity_stock = quantity_stock - %s
                                    WHERE item_number = %s
                                """, (quantity, article))

                            conn.commit()

                            QMessageBox.information(
                                self,
                                "Успех",
                                f"Заказ сохранен с новым номером: {new_order_number}"
                            )
                            self.order_saved.emit()
                            self.close()
                            return

                except Exception as e2:
                    print(f"DEBUG Ошибка при повторной попытке: {e2}")
                    QMessageBox.critical(
                        self,
                        "Ошибка",
                        f"Не удалось сохранить заказ: {str(e2)}\n\n"
                        f"Пожалуйста, закройте и снова откройте окно добавления заказа."
                    )
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {error_msg}")

        except Exception as e:
            # ОТКАТ при любой другой ошибке
            if conn:
                conn.rollback()

            error_msg = str(e)
            print(f"DEBUG Общая ошибка сохранения заказа: {error_msg}")

            # Более информативное сообщение об ошибке
            error_details = str(e)
            if "connection" in error_details.lower():
                QMessageBox.critical(
                    self,
                    "Ошибка подключения",
                    "Не удалось подключиться к базе данных.\n"
                    "Проверьте:\n"
                    "1. Запущен ли PostgreSQL\n"
                    "2. Правильность настроек подключения\n"
                    "3. Существует ли база данных 'shoe_shop'"
                )
            elif "permission" in error_details.lower() or "access" in error_details.lower():
                QMessageBox.critical(
                    self,
                    "Ошибка доступа",
                    "Отказано в доступе к базе данных.\n"
                    "Проверьте логин и пароль пользователя postgres."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Ошибка сохранения заказа:\n{error_details}"
                )

        finally:
            # Всегда закрываем соединения
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_order(self):
        """Удаляет заказ"""
        # Создаем кастомный MessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Подтверждение удаления')
        msg_box.setText('Вы уверены, что хотите удалить этот заказ?\n'
                        'Эта операция необратима и восстановит количество товаров на складе.')
        msg_box.setIcon(QMessageBox.Question)

        # Создаем кнопки с русским текстом
        yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.NoRole)

        # Устанавливаем кнопку по умолчанию
        msg_box.setDefaultButton(no_button)

        # Показываем диалог
        msg_box.exec()

        if msg_box.clickedButton() != yes_button:
            return

        # Если пользователь нажал "Да", продолжаем удаление
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            conn.autocommit = False  # Контролируем транзакцию

            # Сначала восстанавливаем количество товаров на складе
            cursor.execute("""
                SELECT item_number, quantity 
                FROM orders_items 
                WHERE order_number::text = %s
            """, (str(self.order_number),))

            order_items = cursor.fetchall()

            for item_number, quantity in order_items:
                cursor.execute("""
                    UPDATE items 
                    SET quantity_stock = quantity_stock + %s
                    WHERE item_number = %s
                """, (quantity, item_number))

            # Удаляем товары заказа
            cursor.execute("DELETE FROM orders_items WHERE order_number::text = %s", (str(self.order_number),))

            # Удаляем сам заказ (используем текстовое сравнение)
            cursor.execute("DELETE FROM orders WHERE order_number::text = %s", (str(self.order_number),))

            # КОММИТ транзакции
            conn.commit()

            QMessageBox.information(self, "Успех", "Заказ успешно удален")
            self.order_saved.emit()  # Сигнализируем об удалении
            self.close()

        except Exception as e:
            if conn:
                conn.rollback()
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления заказа: {str(e)}")
        finally:
            # Всегда закрываем соединения
            if cursor:
                cursor.close()
            if conn:
                conn.close()

class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.setup_connections()

    def setup_connections(self):
        self.ui.guest_btn.clicked.connect(self.login_as_guest)
        self.ui.login_btn.clicked.connect(self.login)
        self.ui.password_input.returnPressed.connect(self.login)
        self.ui.username_input.returnPressed.connect(self.login)

    def clear_fields(self):
        self.ui.username_input.clear()
        self.ui.password_input.clear()

    def login_as_guest(self):
        self.clear_fields()
        self.main_window.show_catalog("guest", 'Гость')

    def login(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        self.clear_fields()

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT id, login, password, full_name, role
                           FROM users
                           WHERE login = %s
                             AND password = %s
                           """, (username, password))

            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                user_id, login, password, full_name, role = user

                role_clean = role.strip().lower()

                if role_clean == 'авторизированный клиент':
                    self.main_window.show_catalog("client", full_name)
                elif role_clean == "менеджер":
                    self.main_window.show_catalog("manager", full_name)
                elif role_clean == "администратор":
                    self.main_window.show_catalog("admin", full_name)
                else:
                    print(f"Неизвестная роль: {role}")
                    QMessageBox.critical(self, "Ошибка", f"Неизвестная роль пользователя: {role}")

            else:
                QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к БД: {str(e)}")


class GuestCatalogWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.products_data = []

        self.ui = Ui_GuestCatalogWindow()
        self.ui.setupUi(self)

        self.init_ui()
        self.load_products()

    def init_ui(self):
        self.setup_fonts()
        self.setup_logo()
        self.ui.userInfoLabel.setText('Гость')
        self.ui.logoutBtn.clicked.connect(self.main_window.show_login)
        self.ui.productTemplateWidget.setVisible(False)

        self.ui.titleLabel.setMinimumWidth(200)
        self.ui.headerLayout.insertSpacing(1, 5)
        font_metrics = self.ui.userInfoLabel.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.ui.userInfoLabel.text())
        self.ui.userInfoLabel.setFixedWidth(text_width + 10)

        self.right_layout = QHBoxLayout()
        self.right_layout.addWidget(self.ui.logoutBtn)
        self.right_layout.addWidget(self.ui.userInfoLabel)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)

        self.ui.headerLayout.addWidget(right_widget, 0, Qt.AlignmentFlag.AlignRight)
        self.ui.userInfoLabel.setContentsMargins(0, 5, 0, 0)

    def setup_fonts(self):
        title_font = QFont("Times New Roman", 16, QFont.Bold)
        user_font = QFont("Times New Roman", 12)
        button_font = QFont("Times New Roman", 12)

        self.ui.titleLabel.setFont(title_font)
        self.ui.userInfoLabel.setFont(user_font)
        self.ui.logoutBtn.setFont(button_font)

        product_title_font = QFont("Times New Roman", 10, QFont.Bold)
        product_normal_font = QFont("Times New Roman", 9)
        product_small_font = QFont("Times New Roman", 8)
        discount_font = QFont("Times New Roman", 12, QFont.Bold)

        self.ui.templateCategoryNameLabel.setFont(product_title_font)
        self.ui.templateDescriptionLabel.setFont(product_normal_font)
        self.ui.templateManufacturerLabel.setFont(product_normal_font)
        self.ui.templateSupplierLabel.setFont(product_normal_font)
        self.ui.templatePriceLabel.setFont(product_normal_font)
        self.ui.templateUnitLabel.setFont(product_normal_font)
        self.ui.templateQuantityLabel.setFont(product_normal_font)
        self.ui.templateDiscountTitleLabel.setFont(product_small_font)
        self.ui.templateDiscountValueLabel.setFont(discount_font)

    def setup_logo(self):
        try:
            logo_pixmap = QPixmap("import/Icon.png")
            if not logo_pixmap.isNull():

                self.ui.logoLabel.setPixmap(logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio))
                self.ui.logoLabel.setStyleSheet("border: 1px solid black; padding: 3px;")
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            self.ui.logoLabel.setText("ЛОГОТИП")

    def load_products(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT item_number,
                                  name,
                                  item_category,
                                  description,
                                  manufacturer,
                                  provider,
                                  cost,
                                  unit_measurement,
                                  quantity_stock,
                                  current_discount,
                                  photo
                           FROM items
                           ORDER BY name
                           """)
            self.products_data = cursor.fetchall()

            cursor.close()
            conn.close()

            self.display_products(self.products_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров: {str(e)}")

    def create_product_from_template(self, product_data):
        (product_id, name, category, description, manufacturer,
         supplier, price, unit, quantity, discount, image_path) = product_data

        product_widget = QWidget()
        product_widget.setMinimumHeight(140)
        product_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        main_layout = QHBoxLayout(product_widget)
        main_layout.setSpacing(self.ui.productTemplateLayout.spacing())
        main_layout.setContentsMargins(
            self.ui.productTemplateLayout.contentsMargins().left(),
            self.ui.productTemplateLayout.contentsMargins().top(),
            self.ui.productTemplateLayout.contentsMargins().right(),
            self.ui.productTemplateLayout.contentsMargins().bottom()
        )

        photo_label = QLabel()
        photo_label.setMinimumSize(120, 120)
        photo_label.setMaximumSize(120, 120)
        photo_label.setAlignment(Qt.AlignCenter)
        product_pixmap = QPixmap("import/{}".format(image_path))
        scaled_pixmap = product_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        photo_label.setPixmap(scaled_pixmap)
        photo_label.setFixedSize(scaled_pixmap.size())
        photo_label.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        main_layout.addWidget(photo_label)

        center_frame = QFrame()
        center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        center_frame.setFrameShape(self.ui.templateCenterFrame.frameShape())
        center_frame.setFrameShadow(self.ui.templateCenterFrame.frameShadow())

        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(self.ui.templateCenterLayout.spacing())
        center_layout.setContentsMargins(
            self.ui.templateCenterLayout.contentsMargins().left(),
            self.ui.templateCenterLayout.contentsMargins().top(),
            self.ui.templateCenterLayout.contentsMargins().right(),
            self.ui.templateCenterLayout.contentsMargins().bottom()
        )

        category_name_label = QLabel(f"{category} | {name}")
        category_name_label.setFont(self.ui.templateCategoryNameLabel.font())
        category_name_label.setStyleSheet(self.ui.templateCategoryNameLabel.styleSheet())
        category_name_label.setWordWrap(True)
        center_layout.addWidget(category_name_label)

        description_label = QLabel(f"Описание товара: {description}")
        description_label.setFont(self.ui.templateDescriptionLabel.font())
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(40)
        center_layout.addWidget(description_label)

        manufacturer_label = QLabel(f"Производитель: {manufacturer}")
        manufacturer_label.setFont(self.ui.templateManufacturerLabel.font())
        manufacturer_label.setStyleSheet("color: #555555;")
        manufacturer_label.setWordWrap(True)
        center_layout.addWidget(manufacturer_label)

        supplier_label = QLabel(f"Поставщик: {supplier}")
        supplier_label.setFont(self.ui.templateSupplierLabel.font())
        supplier_label.setStyleSheet("color: #555555;")
        supplier_label.setWordWrap(True)
        center_layout.addWidget(supplier_label)

        if discount > 0:
            old_price = price
            new_price = price * (1 - discount / 100)

            if discount > 15:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: white;">{new_price:.2f} ₽</span>'
            else:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: black;">{new_price:.2f} ₽</span>'
        else:
            price_text = f'Цена: {price:.2f} ₽'

        price_label = QLabel()
        price_label.setText(price_text)
        price_label.setFont(self.ui.templatePriceLabel.font())
        price_label.setStyleSheet("")
        price_label.setWordWrap(True)
        center_layout.addWidget(price_label)

        unit_label = QLabel(f"Единица измерения: {unit}")
        unit_label.setFont(self.ui.templateUnitLabel.font())
        unit_label.setStyleSheet("color: #555555;")
        unit_label.setWordWrap(True)
        center_layout.addWidget(unit_label)

        quantity_label = QLabel(f"Количество на складе: {quantity}")
        quantity_label.setFont(self.ui.templateQuantityLabel.font())
        quantity_label.setStyleSheet("color: #555555;")
        quantity_label.setWordWrap(True)
        if quantity == 0:
            quantity_label.setStyleSheet("color: #42AAFF; font-weight: bold;")
        center_layout.addWidget(quantity_label)

        center_layout.addStretch()
        main_layout.addWidget(center_frame)

        discount_layout = QVBoxLayout()
        discount_layout.setSpacing(self.ui.templateDiscountLayout.spacing())
        discount_layout.setAlignment(Qt.AlignCenter)

        discount_title = QLabel("Действующая\nскидка")
        discount_title.setFont(self.ui.templateDiscountTitleLabel.font())
        discount_title.setStyleSheet(self.ui.templateDiscountTitleLabel.styleSheet())
        discount_title.setMinimumSize(100, 30)
        discount_title.setAlignment(Qt.AlignCenter)
        discount_layout.addWidget(discount_title)

        discount_value = QLabel(f"{discount}%")
        discount_value.setFont(self.ui.templateDiscountValueLabel.font())
        discount_value.setMinimumSize(80, 40)
        discount_value.setAlignment(Qt.AlignCenter)

        if discount > 15:
            product_widget.setStyleSheet("""
                background-color: #2E8B57; 
                color: white;
                border: 1px solid #5FCC00; 
                border-radius: 5px;
            """)
            category_name_label.setStyleSheet("color: white; font-weight: bold;")
            description_label.setStyleSheet("color: white;")
            manufacturer_label.setStyleSheet("color: white;")
            supplier_label.setStyleSheet("color: white;")
            unit_label.setStyleSheet("color: white;")
            quantity_label.setStyleSheet("color: white;")
            discount_title.setStyleSheet("color: white; font-weight: bold;")
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")
        elif discount > 0:
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
        else:
            discount_value.setStyleSheet("color: #666; font-size: 16px;")
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)

        discount_layout.addWidget(discount_value)
        main_layout.addLayout(discount_layout)

        return product_widget

    def display_products(self, products):
        layout = self.ui.productsLayout

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        for product_data in products:
            product_widget = self.create_product_from_template(product_data)
            layout.addWidget(product_widget)

        layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_products()


class ClientCatalogWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.products_data = []

        self.ui = Ui_ClientCatalogWindow()
        self.ui.setupUi(self)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Times New Roman';
                color: black;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #7FFF00;
                color: black;
            }
        """)

        self.init_ui()
        self.load_products()

    def set_full_name(self, full_name):
        self.ui.userInfoLabel.setText(full_name)

        font_metrics = self.ui.userInfoLabel.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.ui.userInfoLabel.text())
        self.ui.userInfoLabel.setFixedWidth(text_width + 10)

    def init_ui(self):
        self.setup_fonts()
        self.setup_logo()
        self.ui.logoutBtn.clicked.connect(self.main_window.show_login)
        self.ui.productTemplateWidget.setVisible(False)

        self.ui.titleLabel.setMinimumWidth(200)
        self.ui.headerLayout.insertSpacing(1, 5)

        self.right_layout = QHBoxLayout()
        self.right_layout.addWidget(self.ui.logoutBtn)
        self.right_layout.addWidget(self.ui.userInfoLabel)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)

        self.ui.headerLayout.addWidget(right_widget, 0, Qt.AlignmentFlag.AlignRight)
        self.ui.userInfoLabel.setContentsMargins(0, 5, 0, 0)

    def setup_fonts(self):
        title_font = QFont("Times New Roman", 16, QFont.Bold)
        user_font = QFont("Times New Roman", 12)
        button_font = QFont("Times New Roman", 12)

        self.ui.titleLabel.setFont(title_font)
        self.ui.userInfoLabel.setFont(user_font)
        self.ui.logoutBtn.setFont(button_font)

        product_title_font = QFont("Times New Roman", 10, QFont.Bold)
        product_normal_font = QFont("Times New Roman", 9)
        product_small_font = QFont("Times New Roman", 8)
        discount_font = QFont("Times New Roman", 12, QFont.Bold)

        self.ui.templateCategoryNameLabel.setFont(product_title_font)
        self.ui.templateDescriptionLabel.setFont(product_normal_font)
        self.ui.templateManufacturerLabel.setFont(product_normal_font)
        self.ui.templateSupplierLabel.setFont(product_normal_font)
        self.ui.templatePriceLabel.setFont(product_normal_font)
        self.ui.templateUnitLabel.setFont(product_normal_font)
        self.ui.templateQuantityLabel.setFont(product_normal_font)
        self.ui.templateDiscountTitleLabel.setFont(product_small_font)
        self.ui.templateDiscountValueLabel.setFont(discount_font)

    def setup_logo(self):
        try:
            logo_pixmap = QPixmap("import/Icon.png")
            if not logo_pixmap.isNull():

                self.ui.logoLabel.setPixmap(logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio))
                self.ui.logoLabel.setStyleSheet("border: 1px solid black; padding: 3px;")  # Уменьшил padding
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            self.ui.logoLabel.setText("ЛОГОТИП")

    def load_products(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT item_number,
                                  name,
                                  item_category,
                                  description,
                                  manufacturer,
                                  provider,
                                  cost,
                                  unit_measurement,
                                  quantity_stock,
                                  current_discount,
                                  photo
                           FROM items
                           ORDER BY name
                           """)
            self.products_data = cursor.fetchall()

            cursor.close()
            conn.close()

            self.display_products(self.products_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров: {str(e)}")

    def create_product_from_template(self, product_data):
        (product_id, name, category, description, manufacturer,
         supplier, price, unit, quantity, discount, image_path) = product_data

        product_widget = QWidget()
        product_widget.setMinimumHeight(140)
        product_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        main_layout = QHBoxLayout(product_widget)
        main_layout.setSpacing(self.ui.productTemplateLayout.spacing())
        main_layout.setContentsMargins(
            self.ui.productTemplateLayout.contentsMargins().left(),
            self.ui.productTemplateLayout.contentsMargins().top(),
            self.ui.productTemplateLayout.contentsMargins().right(),
            self.ui.productTemplateLayout.contentsMargins().bottom()
        )

        photo_label = QLabel()
        photo_label.setMinimumSize(120, 120)
        photo_label.setMaximumSize(120, 120)
        photo_label.setAlignment(Qt.AlignCenter)
        product_pixmap = QPixmap("import/{}".format(image_path))
        scaled_pixmap = product_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        photo_label.setPixmap(scaled_pixmap)
        photo_label.setFixedSize(scaled_pixmap.size())
        photo_label.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        main_layout.addWidget(photo_label)

        center_frame = QFrame()
        center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        center_frame.setFrameShape(self.ui.templateCenterFrame.frameShape())
        center_frame.setFrameShadow(self.ui.templateCenterFrame.frameShadow())

        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(self.ui.templateCenterLayout.spacing())
        center_layout.setContentsMargins(
            self.ui.templateCenterLayout.contentsMargins().left(),
            self.ui.templateCenterLayout.contentsMargins().top(),
            self.ui.templateCenterLayout.contentsMargins().right(),
            self.ui.templateCenterLayout.contentsMargins().bottom()
        )

        category_name_label = QLabel(f"{category} | {name}")
        category_name_label.setFont(self.ui.templateCategoryNameLabel.font())
        category_name_label.setStyleSheet(self.ui.templateCategoryNameLabel.styleSheet())
        category_name_label.setWordWrap(True)
        center_layout.addWidget(category_name_label)

        description_label = QLabel(f"Описание товара: {description}")
        description_label.setFont(self.ui.templateDescriptionLabel.font())
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(40)
        center_layout.addWidget(description_label)

        manufacturer_label = QLabel(f"Производитель: {manufacturer}")
        manufacturer_label.setFont(self.ui.templateManufacturerLabel.font())
        manufacturer_label.setStyleSheet("color: #555555;")
        manufacturer_label.setWordWrap(True)
        center_layout.addWidget(manufacturer_label)

        supplier_label = QLabel(f"Поставщик: {supplier}")
        supplier_label.setFont(self.ui.templateSupplierLabel.font())
        supplier_label.setStyleSheet("color: #555555;")
        supplier_label.setWordWrap(True)
        center_layout.addWidget(supplier_label)

        if discount > 0:
            old_price = price
            new_price = price * (1 - discount / 100)

            if discount > 15:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: white;">{new_price:.2f} ₽</span>'
            else:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: black;">{new_price:.2f} ₽</span>'
        else:
            price_text = f'Цена: {price:.2f} ₽'

        price_label = QLabel()
        price_label.setText(price_text)
        price_label.setFont(self.ui.templatePriceLabel.font())
        price_label.setStyleSheet("")
        price_label.setWordWrap(True)
        center_layout.addWidget(price_label)

        unit_label = QLabel(f"Единица измерения: {unit}")
        unit_label.setFont(self.ui.templateUnitLabel.font())
        unit_label.setStyleSheet("color: #555555;")
        unit_label.setWordWrap(True)
        center_layout.addWidget(unit_label)

        quantity_label = QLabel(f"Количество на складе: {quantity}")
        quantity_label.setFont(self.ui.templateQuantityLabel.font())
        quantity_label.setStyleSheet("color: #555555;")
        quantity_label.setWordWrap(True)
        if quantity == 0:
            quantity_label.setStyleSheet("color: #42AAFF; font-weight: bold;")
        center_layout.addWidget(quantity_label)

        center_layout.addStretch()
        main_layout.addWidget(center_frame)

        discount_layout = QVBoxLayout()
        discount_layout.setSpacing(self.ui.templateDiscountLayout.spacing())
        discount_layout.setAlignment(Qt.AlignCenter)

        discount_title = QLabel("Действующая\nскидка")
        discount_title.setFont(self.ui.templateDiscountTitleLabel.font())
        discount_title.setStyleSheet(self.ui.templateDiscountTitleLabel.styleSheet())
        discount_title.setMinimumSize(100, 30)
        discount_title.setAlignment(Qt.AlignCenter)
        discount_layout.addWidget(discount_title)

        discount_value = QLabel(f"{discount}%")
        discount_value.setFont(self.ui.templateDiscountValueLabel.font())
        discount_value.setMinimumSize(80, 40)
        discount_value.setAlignment(Qt.AlignCenter)

        if discount > 15:
            product_widget.setStyleSheet("""
                background-color: #2E8B57; 
                color: white;
                border: 1px solid #5FCC00; 
                border-radius: 5px;
            """)
            category_name_label.setStyleSheet("color: white; font-weight: bold;")
            description_label.setStyleSheet("color: white;")
            manufacturer_label.setStyleSheet("color: white;")
            supplier_label.setStyleSheet("color: white;")
            unit_label.setStyleSheet("color: white;")
            quantity_label.setStyleSheet("color: white;")
            discount_title.setStyleSheet("color: white; font-weight: bold;")
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")
        elif discount > 0:
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
        else:
            discount_value.setStyleSheet("color: #666; font-size: 16px;")
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)

        discount_layout.addWidget(discount_value)
        main_layout.addLayout(discount_layout)

        return product_widget

    def display_products(self, products):
        layout = self.ui.productsLayout

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        for product_data in products:
            product_widget = self.create_product_from_template(product_data)
            layout.addWidget(product_widget)

        layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_products()


class ManagerCatalogWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.products_data = []
        self.all_suppliers = []
        self.orders_data = []

        self.ui = Ui_ManagerCatalogWindow()
        self.ui.setupUi(self)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Times New Roman';
                color: black;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #7FFF00;
                color: black;
            }
        """)

        self.init_ui()
        self.load_products()
        self.load_orders()

    def set_full_name(self, full_name):
        self.ui.userInfoLabel.setText(full_name)

        font_metrics = self.ui.userInfoLabel.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.ui.userInfoLabel.text())
        self.ui.userInfoLabel.setFixedWidth(text_width + 10)

    def init_ui(self):
        self.setup_fonts()
        self.setup_logo()
        self.ui.logoutBtn.clicked.connect(self.main_window.show_login)

        self.ui.titleLabel.setMinimumWidth(200)
        self.ui.headerLayout.insertSpacing(1, 5)

        self.right_layout = QHBoxLayout()
        self.right_layout.addWidget(self.ui.logoutBtn)
        self.right_layout.addWidget(self.ui.userInfoLabel)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)

        self.ui.headerLayout.addWidget(right_widget, 0, Qt.AlignmentFlag.AlignRight)
        self.ui.userInfoLabel.setContentsMargins(0, 5, 0, 0)

        self.products_search = self.ui.productsSearch
        self.products_sort = self.ui.productsSort
        self.products_filter = self.ui.productsFilter

        self.products_search.setMinimumWidth(300)
        self.products_search.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.products_search.textChanged.connect(self.apply_product_filters)
        self.products_sort.currentIndexChanged.connect(self.apply_product_filters)
        self.products_filter.currentIndexChanged.connect(self.apply_product_filters)

        self.products_layout = self.ui.productsLayout
        self.orders_layout = self.ui.ordersLayout

    def setup_fonts(self):
        title_font = QFont("Times New Roman", 16, QFont.Bold)
        user_font = QFont("Times New Roman", 12)
        button_font = QFont("Times New Roman", 12)

        self.ui.titleLabel.setFont(title_font)
        self.ui.userInfoLabel.setFont(user_font)
        self.ui.logoutBtn.setFont(button_font)


    def setup_logo(self):
        try:
            logo_pixmap = QPixmap("import/Icon.png")
            if not logo_pixmap.isNull():

                scaled_pixmap = logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                self.ui.logoLabel.setPixmap(scaled_pixmap)
                self.ui.logoLabel.setStyleSheet("border: 1px solid black; padding: 3px;")
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            self.ui.logoLabel.setText("ЛОГОТИП")

    def load_products(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT item_number,
                                  name,
                                  item_category,
                                  description,
                                  manufacturer,
                                  provider,
                                  cost,
                                  unit_measurement,
                                  quantity_stock,
                                  current_discount,
                                  photo
                           FROM items
                           ORDER BY name
                           """)
            self.products_data = cursor.fetchall()

            cursor.execute("SELECT DISTINCT provider FROM items WHERE provider IS NOT NULL ORDER BY provider")
            suppliers = cursor.fetchall()
            self.all_suppliers = [supplier[0] for supplier in suppliers]

            cursor.close()
            conn.close()

            self.products_filter.clear()
            self.products_filter.addItem("Все поставщики")
            for supplier in self.all_suppliers:
                self.products_filter.addItem(supplier)

            self.display_products(self.products_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров: {str(e)}")

    def apply_product_filters(self):
        search_text = self.products_search.text().lower()
        sort_index = self.products_sort.currentIndex()
        filter_supplier = self.products_filter.currentText()

        filtered_products = self.products_data.copy()

        if search_text:
            search_terms = search_text.lower().split()

            def matches_all_terms(product):
                product_fields = [
                    str(product[1]).lower(),
                    str(product[2]).lower(),
                    str(product[3]).lower(),
                    str(product[4]).lower(),
                    str(product[5]).lower()
                ]

                return all(
                    any(term in field for field in product_fields)
                    for term in search_terms
                )

            filtered_products = [product for product in filtered_products if matches_all_terms(product)]

        if filter_supplier != "Все поставщики":
            filtered_products = [
                product for product in filtered_products
                if product[5] == filter_supplier
            ]

        if sort_index == 1:
            filtered_products.sort(key=lambda x: x[8])
        elif sort_index == 2:
            filtered_products.sort(key=lambda x: x[8], reverse=True)

        self.display_products(filtered_products)

    def display_products(self, products):
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not products:
            no_products_label = QLabel("Товары не найдены")
            no_products_label.setAlignment(Qt.AlignCenter)
            no_products_label.setStyleSheet("font-size: 14px; color: gray; margin: 20px;")
            self.products_layout.addWidget(no_products_label)
        else:
            for product_data in products:
                product_widget = self.create_product_widget(product_data)
                self.products_layout.addWidget(product_widget)

        self.products_layout.addStretch()

    def create_product_widget(self, product_data):
        (product_id, name, category, description, manufacturer,
         supplier, price, unit, quantity, discount, image_path) = product_data

        product_widget = QWidget()
        product_widget.setMinimumHeight(140)
        product_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        main_layout = QHBoxLayout(product_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 10, 15, 10)

        photo_label = QLabel()
        photo_label.setMinimumSize(120, 120)
        photo_label.setMaximumSize(120, 120)
        photo_label.setAlignment(Qt.AlignCenter)
        product_pixmap = QPixmap("import/{}".format(image_path))
        scaled_pixmap = product_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        photo_label.setPixmap(scaled_pixmap)
        photo_label.setFixedSize(scaled_pixmap.size())
        photo_label.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        main_layout.addWidget(photo_label)

        center_frame = QFrame()
        center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        center_frame.setFrameShape(QFrame.Shape.NoFrame)

        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(4)
        center_layout.setContentsMargins(8, 0, 8, 0)

        category_name_label = QLabel(f"{category} | {name}")
        category_name_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        category_name_label.setStyleSheet("font-weight: bold; color: #333333;")
        category_name_label.setWordWrap(True)
        center_layout.addWidget(category_name_label)

        description_label = QLabel(f"Описание товара: {description}")
        description_label.setFont(QFont("Times New Roman", 9))
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(40)
        center_layout.addWidget(description_label)

        manufacturer_label = QLabel(f"Производитель: {manufacturer}")
        manufacturer_label.setFont(QFont("Times New Roman", 9))
        manufacturer_label.setStyleSheet("color: #555555;")
        manufacturer_label.setWordWrap(True)
        center_layout.addWidget(manufacturer_label)

        supplier_label = QLabel(f"Поставщик: {supplier}")
        supplier_label.setFont(QFont("Times New Roman", 9))
        supplier_label.setStyleSheet("color: #555555;")
        supplier_label.setWordWrap(True)
        center_layout.addWidget(supplier_label)

        if discount > 0:
            old_price = price
            new_price = price * (1 - discount / 100)

            if discount > 15:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: white;">{new_price:.2f} ₽</span>'
            else:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: black;">{new_price:.2f} ₽</span>'
        else:
            price_text = f'Цена: {price:.2f} ₽'

        price_label = QLabel()
        price_label.setText(price_text)
        price_label.setFont(QFont("Times New Roman", 9))
        price_label.setStyleSheet("")
        price_label.setWordWrap(True)
        center_layout.addWidget(price_label)

        unit_label = QLabel(f"Единица измерения: {unit}")
        unit_label.setFont(QFont("Times New Roman", 9))
        unit_label.setStyleSheet("color: #555555;")
        unit_label.setWordWrap(True)
        center_layout.addWidget(unit_label)

        quantity_label = QLabel(f"Количество на складе: {quantity}")
        quantity_label.setFont(QFont("Times New Roman", 9))
        quantity_label.setStyleSheet("color: #555555;")
        quantity_label.setWordWrap(True)
        if quantity == 0:
            quantity_label.setStyleSheet("color: #42AAFF; font-weight: bold;")
        center_layout.addWidget(quantity_label)

        center_layout.addStretch()
        main_layout.addWidget(center_frame)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)
        right_panel.setAlignment(Qt.AlignCenter)

        discount_layout = QVBoxLayout()
        discount_layout.setSpacing(5)
        discount_layout.setAlignment(Qt.AlignCenter)

        discount_title = QLabel("Действующая\nскидка")
        discount_title.setFont(QFont("Times New Roman", 8))
        discount_title.setStyleSheet("font-weight: bold; color: #333333;")
        discount_title.setMinimumSize(100, 30)
        discount_title.setAlignment(Qt.AlignCenter)
        discount_layout.addWidget(discount_title)

        discount_value = QLabel(f"{discount}%")
        discount_value.setFont(QFont("Times New Roman", 12, QFont.Bold))
        discount_value.setMinimumSize(80, 40)
        discount_value.setAlignment(Qt.AlignCenter)

        if discount > 15:
            product_widget.setStyleSheet("""
                background-color: #2E8B57; 
                color: white;
                border: 1px solid #5FCC00; 
                border-radius: 5px;
            """)
            category_name_label.setStyleSheet("color: white; font-weight: bold;")
            description_label.setStyleSheet("color: white;")
            manufacturer_label.setStyleSheet("color: white;")
            supplier_label.setStyleSheet("color: white;")
            unit_label.setStyleSheet("color: white;")
            quantity_label.setStyleSheet("color: white;")
            discount_title.setStyleSheet("color: white; font-weight: bold;")
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")  # Изменено на красный
        elif discount > 0:
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")  # Зеленый
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
        else:
            discount_value.setStyleSheet("color: #666; font-size: 16px;")  # Серый
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)

        discount_layout.addWidget(discount_value)
        main_layout.addLayout(discount_layout)

        return product_widget

    def load_orders(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT o.order_number,
                                  o.order_date,
                                  o.delivery_date,
                                  o.order_status,
                                  pp.address
                           FROM orders o
                                    LEFT JOIN pickup_points pp ON o.id_pickup_point = pp.id
                           ORDER BY o.order_date DESC
                           """)
            orders_raw = cursor.fetchall()
            self.orders_data = [list(order) for order in orders_raw]

            cursor.execute("""
                           SELECT oi.order_number,
                                  oi.item_number,
                                  oi.quantity
                           FROM orders_items oi
                                    JOIN orders o ON oi.order_number = o.order_number
                           """)
            self.orders_items_data = cursor.fetchall()
            for order_item in self.orders_items_data:
                order_number, item_number, quantity = order_item
                for order in self.orders_data:
                    if order_number == order[0]:
                        if len(order) != 6:
                            order.append(f"{item_number}#{quantity}")
                        else:
                            order[5] += f"{item_number}#{quantity}"

            cursor.close()
            conn.close()

            self.display_orders(self.orders_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки заказов: {str(e)}")

    def display_orders(self, orders):
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not orders:
            no_orders_label = QLabel("Заказы не найдены")
            no_orders_label.setAlignment(Qt.AlignCenter)
            no_orders_label.setStyleSheet("font-size: 14px; color: gray; margin: 20px;")
            self.orders_layout.addWidget(no_orders_label)
        else:
            for order_data in orders:
                order_widget = self.create_order_widget(order_data)
                self.orders_layout.addWidget(order_widget)

        self.orders_layout.addStretch()

    def create_order_widget(self, order_data):
        (order_number, order_date, delivery_date, order_status, address, order_article) = order_data

        order_widget = QWidget()
        order_widget.setFixedHeight(140)
        order_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        main_layout = QHBoxLayout(order_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 10, 15, 10)

        center_frame = QFrame()
        center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        center_frame.setFrameShape(QFrame.Shape.NoFrame)
        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(4)
        center_layout.setContentsMargins(8, 0, 8, 0)
        center_layout.setAlignment(Qt.AlignTop)

        order_number_label = QLabel(f"Артикул заказа: {order_article}")
        order_number_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        order_number_label.setStyleSheet("font-weight: bold; color: #333333;")
        order_number_label.setWordWrap(True)
        center_layout.addWidget(order_number_label)

        status_label = QLabel(f"Статус: {order_status}")
        status_label.setFont(QFont("Times New Roman", 10))
        status_label.setWordWrap(True)
        center_layout.addWidget(status_label)

        address_text = f"Адрес пункта выдачи: {address}" if address else "Адрес пункта выдачи: не указан"
        address_label = QLabel(address_text)
        address_label.setFont(QFont("Times New Roman", 10))
        address_label.setWordWrap(True)
        address_label.setMaximumHeight(35)
        center_layout.addWidget(address_label)

        order_date_str = order_date.strftime("%Y-%m-%d") if order_date else "Не указана"
        date_label = QLabel(f"Дата заказа: {order_date_str}")
        date_label.setFont(QFont("Times New Roman", 10))
        date_label.setStyleSheet("color: #555555;")
        date_label.setWordWrap(True)
        center_layout.addWidget(date_label)

        main_layout.addWidget(center_frame, 1)

        delivery_layout = QVBoxLayout()
        delivery_layout.setSpacing(2)
        delivery_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        delivery_title = QLabel("Дата")
        delivery_title.setFont(QFont("Times New Roman", 10))
        delivery_title.setAlignment(Qt.AlignCenter)
        delivery_layout.addWidget(delivery_title)

        delivery_subtitle = QLabel("доставки")
        delivery_subtitle.setFont(QFont("Times New Roman", 10))
        delivery_subtitle.setAlignment(Qt.AlignCenter)
        delivery_layout.addWidget(delivery_subtitle)

        delivery_date_str = delivery_date.strftime("%Y-%m-%d") if delivery_date else "Не указана"
        delivery_value = QLabel(delivery_date_str)
        delivery_value.setFont(QFont("Times New Roman", 14, QFont.Bold))
        delivery_value.setFixedSize(100, 40)
        delivery_value.setAlignment(Qt.AlignCenter)
        delivery_layout.addWidget(delivery_value)

        main_layout.addLayout(delivery_layout)

        order_widget.setStyleSheet("""
             QWidget {
                 background-color: white;
                 border: 1px solid #ddd;
                 border-radius: 5px;
             }
         """)

        return order_widget

    def showEvent(self, event):
        super().showEvent(event)
        self.load_products()
        self.load_orders()


class AdminCatalogWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.products_data = []
        self.all_suppliers = []
        self.orders_data = []
        self.product_window = None
        self.order_window = None

        self.ui = Ui_AdminCatalogWindow()
        self.ui.setupUi(self)
        self.ui.testOrdersBtn.clicked.connect(self.open_tests_window)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Times New Roman';
                color: black;
            }
            QLabel {
                color: black;
            }
        """)

        self.init_ui()
        self.load_products()
        self.load_orders()

    def set_full_name(self, full_name):
        self.ui.userInfoLabel.setText(full_name)

        font_metrics = self.ui.userInfoLabel.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.ui.userInfoLabel.text())
        self.ui.userInfoLabel.setFixedWidth(text_width + 10)

    def init_ui(self):
        self.setup_fonts()
        self.setup_logo()

        self.ui.logoutBtn.clicked.connect(self.main_window.show_login)
        self.ui.addProductBtn.clicked.connect(self.open_add_product_window)
        self.ui.addOrderBtn.clicked.connect(self.open_add_order_window)
        self.ui.deleteProductBtn.clicked.connect(lambda: self.delete_selected_product())

        self.ui.titleLabel.setMinimumWidth(200)
        self.ui.headerLayout.insertSpacing(1, 5)

        self.right_layout = QHBoxLayout()
        self.right_layout.addWidget(self.ui.logoutBtn)
        self.right_layout.addWidget(self.ui.userInfoLabel)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)

        self.ui.headerLayout.addWidget(right_widget, 0, Qt.AlignmentFlag.AlignRight)
        self.ui.userInfoLabel.setContentsMargins(0, 5, 0, 0)

        self.products_search = self.ui.productsSearch
        self.products_sort = self.ui.productsSort
        self.products_filter = self.ui.productsFilter
        self.products_layout = self.ui.productsLayout
        self.orders_layout = self.ui.ordersLayout

        self.products_search.setMinimumWidth(300)
        self.products_search.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.products_search.textChanged.connect(self.apply_product_filters)
        self.products_sort.currentIndexChanged.connect(self.apply_product_filters)
        self.products_filter.currentIndexChanged.connect(self.apply_product_filters)

    def setup_fonts(self):
        title_font = QFont("Times New Roman", 16, QFont.Bold)
        user_font = QFont("Times New Roman", 12)
        button_font = QFont("Times New Roman", 12)

        self.ui.titleLabel.setFont(title_font)
        self.ui.userInfoLabel.setFont(user_font)
        self.ui.logoutBtn.setFont(button_font)
        self.ui.addProductBtn.setFont(button_font)
        self.ui.addOrderBtn.setFont(button_font)
        self.ui.deleteProductBtn.setFont(button_font)

    def setup_logo(self):
        try:
            logo_pixmap = QPixmap("import/Icon.png")
            if not logo_pixmap.isNull():

                scaled_pixmap = logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                self.ui.logoLabel.setPixmap(scaled_pixmap)
                self.ui.logoLabel.setStyleSheet("border: 1px solid black; padding: 3px;")
        except Exception as e:
            print(f"Ошибка загрузки логотипа: {e}")
            self.ui.logoLabel.setText("ЛОГОТИП")

    def open_tests_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Тестирование заказов")
        dialog.setMinimumSize(300, 200)

        layout = QVBoxLayout(dialog)

        positive_btn = QPushButton("Позитивный тест")
        negative_btn = QPushButton("Негативный тест")

        positive_btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                font-weight: bold;
                padding: 10px;
            }
        """)

        negative_btn.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
                font-weight: bold;
                padding: 10px;
            }
        """)

        positive_btn.clicked.connect(lambda: self.run_positive_test(dialog))
        negative_btn.clicked.connect(lambda: self.run_negative_test(dialog))

        layout.addWidget(positive_btn)
        layout.addWidget(negative_btn)

        dialog.exec()

    def run_positive_test(self, dialog):
        from order_tests import OrderTests

        tests = OrderTests()
        success, message = tests.positive_test()
        tests.close()

        if success:
            QMessageBox.information(self, "Успех", message)
            QTimer.singleShot(0, self.load_orders)
            dialog.accept()
        else:
            QMessageBox.critical(self, "Ошибка", message)

    def run_negative_test(self, dialog):
        from order_tests import OrderTests

        tests = OrderTests()
        success, message = tests.negative_test()
        tests.close()

        QMessageBox.critical(
            self,
            "Ошибка тестирования",
            message
        )

    def load_products(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT item_number,
                                  name,
                                  item_category,
                                  description,
                                  manufacturer,
                                  provider,
                                  cost,
                                  unit_measurement,
                                  quantity_stock,
                                  current_discount,
                                  photo
                           FROM items
                           ORDER BY name
                           """)
            self.products_data = cursor.fetchall()

            cursor.execute("SELECT DISTINCT provider FROM items WHERE provider IS NOT NULL ORDER BY provider")
            suppliers = cursor.fetchall()
            self.all_suppliers = [supplier[0] for supplier in suppliers]

            cursor.close()
            conn.close()

            self.products_filter.clear()
            self.products_filter.addItem("Все поставщики")
            for supplier in self.all_suppliers:
                self.products_filter.addItem(supplier)

            self.display_products(self.products_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров: {str(e)}")

    def apply_product_filters(self):
        search_text = self.products_search.text().lower()
        sort_index = self.products_sort.currentIndex()
        filter_supplier = self.products_filter.currentText()

        filtered_products = self.products_data.copy()

        if search_text:
            search_terms = search_text.lower().split()

            def matches_all_terms(product):
                product_fields = [
                    str(product[1]).lower(),
                    str(product[2]).lower(),
                    str(product[3]).lower(),
                    str(product[4]).lower(),
                    str(product[5]).lower()
                ]

                return all(
                    any(term in field for field in product_fields)
                    for term in search_terms
                )

            filtered_products = [product for product in filtered_products if matches_all_terms(product)]

        if filter_supplier != "Все поставщики":
            filtered_products = [
                product for product in filtered_products
                if product[5] == filter_supplier
            ]

        if sort_index == 1:
            filtered_products.sort(key=lambda x: x[8])
        elif sort_index == 2:
            filtered_products.sort(key=lambda x: x[8], reverse=True)

        self.display_products(filtered_products)

    def display_products(self, products):
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not products:
            no_products_label = QLabel("Товары не найдены")
            no_products_label.setAlignment(Qt.AlignCenter)
            no_products_label.setStyleSheet("font-size: 14px; color: gray; margin: 20px;")
            self.products_layout.addWidget(no_products_label)
        else:
            for product_data in products:
                product_widget = self.create_product_widget(product_data)
                self.products_layout.addWidget(product_widget)

        self.products_layout.addStretch()

    def create_product_widget(self, product_data):
        (product_id, name, category, description, manufacturer,
         supplier, price, unit, quantity, discount, image_path) = product_data

        product_widget = QWidget()
        product_widget.setMinimumHeight(140)
        product_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        product_widget.setCursor(Qt.PointingHandCursor)
        product_widget.mousePressEvent = lambda event: self.on_product_widget_clicked(event, product_id)

        main_layout = QHBoxLayout(product_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 10, 15, 10)

        photo_label = QLabel()
        photo_label.setMinimumSize(120, 120)
        photo_label.setMaximumSize(120, 120)
        photo_label.setAlignment(Qt.AlignCenter)
        try:
            product_pixmap = QPixmap("import/{}".format(image_path))
            scaled_pixmap = product_pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            photo_label.setPixmap(scaled_pixmap)
            photo_label.setFixedSize(scaled_pixmap.size())
        except:
            photo_label.setText("Нет фото")
            photo_label.setStyleSheet(
                "border: 1px solid #ccc; background-color: white; font-weight: bold; color: black;")
        photo_label.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        main_layout.addWidget(photo_label)

        center_frame = QFrame()
        center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        center_frame.setFrameShape(QFrame.Shape.NoFrame)
        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(4)
        center_layout.setContentsMargins(8, 0, 8, 0)

        category_name_label = QLabel(f"{category} | {name}")
        category_name_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        category_name_label.setStyleSheet("font-weight: bold; color: #333333;")
        category_name_label.setWordWrap(True)
        center_layout.addWidget(category_name_label)

        description_label = QLabel(f"Описание товара: {description}")
        description_label.setFont(QFont("Times New Roman", 9))
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(40)
        center_layout.addWidget(description_label)

        manufacturer_label = QLabel(f"Производитель: {manufacturer}")
        manufacturer_label.setFont(QFont("Times New Roman", 9))
        manufacturer_label.setStyleSheet("color: #555555;")
        manufacturer_label.setWordWrap(True)
        center_layout.addWidget(manufacturer_label)

        supplier_label = QLabel(f"Поставщик: {supplier}")
        supplier_label.setFont(QFont("Times New Roman", 9))
        supplier_label.setStyleSheet("color: #555555;")
        supplier_label.setWordWrap(True)
        center_layout.addWidget(supplier_label)

        if discount > 0:
            old_price = price
            new_price = price * (1 - discount / 100)

            if discount > 15:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: white;">{new_price:.2f} ₽</span>'
            else:
                price_text = f'Цена: <span style="color: red; text-decoration: line-through;">{old_price:.2f} ₽</span> <span style="color: black;">{new_price:.2f} ₽</span>'
        else:
            price_text = f'Цена: {price:.2f} ₽'

        price_label = QLabel()
        price_label.setText(price_text)
        price_label.setFont(QFont("Times New Roman", 9))
        price_label.setStyleSheet("")
        price_label.setWordWrap(True)
        center_layout.addWidget(price_label)

        unit_label = QLabel(f"Единица измерения: {unit}")
        unit_label.setFont(QFont("Times New Roman", 9))
        unit_label.setStyleSheet("color: #555555;")
        unit_label.setWordWrap(True)
        center_layout.addWidget(unit_label)

        quantity_label = QLabel(f"Количество на складе: {quantity}")
        quantity_label.setFont(QFont("Times New Roman", 9))
        quantity_label.setStyleSheet("color: #555555;")
        quantity_label.setWordWrap(True)
        if quantity == 0:
            quantity_label.setStyleSheet("color: #42AAFF; font-weight: bold;")
        center_layout.addWidget(quantity_label)

        center_layout.addStretch()
        main_layout.addWidget(center_frame)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)
        right_panel.setAlignment(Qt.AlignCenter)

        discount_layout = QVBoxLayout()
        discount_layout.setSpacing(5)
        discount_layout.setAlignment(Qt.AlignCenter)

        discount_title = QLabel("Действующая\nскидка")
        discount_title.setFont(QFont("Times New Roman", 8))
        discount_title.setStyleSheet("font-weight: bold; color: #333333;")
        discount_title.setMinimumSize(100, 30)
        discount_title.setAlignment(Qt.AlignCenter)
        discount_layout.addWidget(discount_title)

        discount_value = QLabel(f"{discount}%")
        discount_value.setFont(QFont("Times New Roman", 12, QFont.Bold))
        discount_value.setMinimumSize(80, 40)
        discount_value.setAlignment(Qt.AlignCenter)

        if discount > 15:
            product_widget.setStyleSheet("""
                background-color: #2E8B57; 
                color: white;
                border: 1px solid #5FCC00; 
                border-radius: 5px;
            """)
            category_name_label.setStyleSheet("color: white; font-weight: bold;")
            description_label.setStyleSheet("color: white;")
            manufacturer_label.setStyleSheet("color: white;")
            supplier_label.setStyleSheet("color: white;")
            unit_label.setStyleSheet("color: white;")
            quantity_label.setStyleSheet("color: white;")
            discount_title.setStyleSheet("color: white; font-weight: bold;")
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")
        elif discount > 0:
            discount_value.setStyleSheet(
                "color: #7FFF00; font-weight: bold; font-size: 16px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);")
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
        else:
            discount_value.setStyleSheet("color: #666; font-size: 16px;")
            discount_title.setStyleSheet("color: #333333; font-weight: bold;")

            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)

        discount_layout.addWidget(discount_value)
        right_panel.addLayout(discount_layout)

        delete_btn = QPushButton("Удалить")
        delete_btn.setToolTip("Удалить товар")
        delete_btn.setMinimumSize(120, 30)
        delete_btn.setFont(QFont("Times New Roman", 10))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: black;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #6EEF00;
            }
            QPushButton:pressed {
                background-color: #00FA9A;
            }
        """)
        delete_btn.clicked.connect(lambda checked, pid=str(product_id), pname=name: self.delete_product(pid, pname))
        right_panel.addWidget(delete_btn)

        main_layout.addLayout(right_panel)

        if discount <= 15:
            product_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)

        return product_widget

    def on_product_widget_clicked(self, event, product_id):
        if event.button() == Qt.LeftButton:
            self.open_edit_product_window(product_id)

    def load_orders(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT o.order_number,
                                  o.order_date,
                                  o.delivery_date,
                                  o.order_status,
                                  pp.address
                           FROM orders o
                                    LEFT JOIN pickup_points pp ON o.id_pickup_point = pp.id
                           ORDER BY o.order_date DESC
                           """)
            orders_raw = cursor.fetchall()
            self.orders_data = [list(order) for order in orders_raw]

            cursor.execute("""
                           SELECT oi.order_number,
                                  oi.item_number,
                                  oi.quantity
                           FROM orders_items oi
                                    JOIN orders o ON oi.order_number = o.order_number
                           """)
            self.orders_items_data = cursor.fetchall()
            for order_item in self.orders_items_data:
                order_number, item_number, quantity = order_item
                for order in self.orders_data:
                    if order_number == order[0]:
                        if len(order) != 6:
                            order.append(f"{item_number}#{quantity}")
                        else:
                            order[5] += f"{item_number}#{quantity}"

            cursor.close()
            conn.close()

            self.display_orders(self.orders_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки заказов: {str(e)}")

    def display_orders(self, orders):
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not orders:
            no_orders_label = QLabel("Заказы не найдены")
            no_orders_label.setAlignment(Qt.AlignCenter)
            no_orders_label.setStyleSheet("font-size: 14px; color: gray; margin: 20px;")
            self.orders_layout.addWidget(no_orders_label)
        else:
            for order_data in orders:
                order_widget = self.create_order_widget(order_data)
                self.orders_layout.addWidget(order_widget)

        self.orders_layout.addStretch()

    def create_order_widget(self, order_data):
        (order_number, order_date, delivery_date, order_status, address, order_article) = order_data

        order_widget = QWidget()
        order_widget.setFixedHeight(140)  # Фиксированная высота как у менеджера
        order_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        main_layout = QHBoxLayout(order_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 10, 15, 10)

        center_frame = QFrame()
        center_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        center_frame.setFrameShape(QFrame.Shape.NoFrame)
        center_layout = QVBoxLayout(center_frame)
        center_layout.setSpacing(4)
        center_layout.setContentsMargins(8, 0, 8, 0)
        center_layout.setAlignment(Qt.AlignTop)

        order_number_label = QLabel(f"Артикул заказа: {order_article}")
        order_number_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        order_number_label.setStyleSheet("font-weight: bold; color: #333333;")
        order_number_label.setWordWrap(True)
        center_layout.addWidget(order_number_label)

        status_label = QLabel(f"Статус: {order_status}")
        status_label.setFont(QFont("Times New Roman", 10))
        status_label.setWordWrap(True)
        center_layout.addWidget(status_label)

        address_text = f"Адрес пункта выдачи: {address}" if address else "Адрес пункта выдачи: не указан"
        address_label = QLabel(address_text)
        address_label.setFont(QFont("Times New Roman", 10))
        address_label.setWordWrap(True)
        address_label.setMaximumHeight(35)
        center_layout.addWidget(address_label)

        order_date_str = order_date.strftime("%Y-%m-%d") if order_date else "Не указана"
        date_label = QLabel(f"Дата заказа: {order_date_str}")
        date_label.setFont(QFont("Times New Roman", 10))
        date_label.setStyleSheet("color: #555555;")
        date_label.setWordWrap(True)
        center_layout.addWidget(date_label)

        main_layout.addWidget(center_frame, 1)

        delivery_layout = QVBoxLayout()
        delivery_layout.setSpacing(2)
        delivery_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        delivery_title = QLabel("Дата")
        delivery_title.setFont(QFont("Times New Roman", 10))
        delivery_title.setAlignment(Qt.AlignCenter)
        delivery_layout.addWidget(delivery_title)

        delivery_subtitle = QLabel("доставки")
        delivery_subtitle.setFont(QFont("Times New Roman", 10))
        delivery_subtitle.setAlignment(Qt.AlignCenter)
        delivery_layout.addWidget(delivery_subtitle)

        delivery_date_str = delivery_date.strftime("%Y-%m-%d") if delivery_date else "Не указана"
        delivery_value = QLabel(delivery_date_str)
        delivery_value.setFont(QFont("Times New Roman", 14, QFont.Bold))
        delivery_value.setFixedSize(100, 40)
        delivery_value.setAlignment(Qt.AlignCenter)
        delivery_layout.addWidget(delivery_value)

        main_layout.addLayout(delivery_layout)

        order_widget.setStyleSheet("""
             QWidget {
                 background-color: white;
                 border: 1px solid #ddd;
                 border-radius: 5px;
             }
         """)

        order_widget.setCursor(Qt.PointingHandCursor)
        order_widget.mousePressEvent = lambda event: self.on_order_widget_clicked(event, order_number)

        return order_widget

    def on_order_widget_clicked(self, event, order_number):
        if event.button() == Qt.LeftButton:
            self.open_edit_order_window(order_number)

    def open_add_product_window(self):
        if self.product_window is not None:
            self.product_window.activateWindow()
            self.product_window.raise_()
            QMessageBox.warning(self, "Внимание", "Окно редактирования товара уже открыто")
            return

        self.product_window = ProductEditWindow(mode='add', parent=self)
        self.product_window.product_saved.connect(self.load_products)
        self.product_window.closed.connect(self.on_product_window_closed)
        self.product_window.show()

    def open_edit_product_window(self, product_id):
        if self.product_window is not None:
            self.product_window.activateWindow()
            self.product_window.raise_()
            QMessageBox.warning(self, "Внимание", "Окно редактирования товара уже открыто")
            return

        try:
            self.product_window = ProductEditWindow(mode='edit', product_id=product_id, parent=self)
            self.product_window.product_saved.connect(self.load_products)
            self.product_window.closed.connect(self.on_product_window_closed)
            self.product_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Неверный ID товара: {product_id}")

    def open_add_order_window(self):
        if self.order_window is not None:
            self.order_window.activateWindow()
            self.order_window.raise_()
            QMessageBox.warning(self, "Внимание", "Окно редактирования заказа уже открыто")
            return

        self.order_window = OrderEditWindow(mode='add', parent=self)
        self.order_window.order_saved.connect(self.load_orders)
        self.order_window.closed.connect(self.on_order_window_closed)
        self.order_window.show()

    def open_edit_order_window(self, order_number):
        if self.order_window is not None:
            self.order_window.activateWindow()
            self.order_window.raise_()
            QMessageBox.warning(self, "Внимание", "Окно редактирования заказа уже открыто")
            return

        try:
            self.order_window = OrderEditWindow(mode='edit', order_number=order_number, parent=self)
            self.order_window.order_saved.connect(self.load_orders)
            self.order_window.closed.connect(self.on_order_window_closed)
            self.order_window.show()
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка открытия окна редактирования: {str(e)}")

    def on_product_window_closed(self):
        self.product_window = None

    def on_order_window_closed(self):
        self.order_window = None

    def delete_product(self, product_id, product_name):
        try:
            # Создаем кастомный MessageBox
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Подтверждение удаления')
            msg_box.setText(f'Вы уверены, что хотите удалить товар "{product_name}"?\n'
                            f'Эта операция необратима и удалит связанное изображение.')
            msg_box.setIcon(QMessageBox.Question)

            # Создаем кнопки с русским текстом
            yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
            no_button = msg_box.addButton("Нет", QMessageBox.NoRole)

            # Устанавливаем кнопку по умолчанию
            msg_box.setDefaultButton(no_button)

            # Показываем диалог
            msg_box.exec()

            if msg_box.clickedButton() != yes_button:
                return

            # Если пользователь нажал "Да", продолжаем удаление
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT photo FROM items WHERE item_number = %s", (product_id,))
            result = cursor.fetchone()

            photo_to_delete = None
            if result and result[0]:
                photo_to_delete = result[0]

            cursor.execute("DELETE FROM items WHERE item_number = %s", (product_id,))
            conn.commit()
            cursor.close()
            conn.close()

            if photo_to_delete and photo_to_delete.lower() != 'picture.png':
                photo_path = os.path.join("import", str(photo_to_delete))
                if os.path.exists(photo_path) and os.path.isfile(photo_path):
                    try:
                        os.remove(photo_path)
                    except Exception as img_error:
                        print(f"Ошибка при удалении изображения: {img_error}")
            elif photo_to_delete and photo_to_delete.lower() == 'picture.png':
                print("Дефолтное изображение picture.png не удаляется")

            QMessageBox.information(None, "Успех", f"Товар '{product_name}' успешно удален")
            self.load_products()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления товара: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_products()
        self.load_orders()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        self.setStyleSheet("""
            background-color: white;
            font-family: 'Times New Roman';
            color: black;
        """)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_window = LoginWindow(self)

        self.guest_window = GuestCatalogWindow(self)
        self.client_window = ClientCatalogWindow(self)
        self.manager_window = ManagerCatalogWindow(self)
        self.admin_window = AdminCatalogWindow(self)

        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.guest_window)
        self.stacked_widget.addWidget(self.client_window)
        self.stacked_widget.addWidget(self.manager_window)
        self.stacked_widget.addWidget(self.admin_window)

        self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.setWindowTitle("Авторизация")
        self.setWindowIcon(QIcon("import/Icon.png"))

    def show_catalog(self, user_type, full_name):
        self.setWindowTitle("Каталог")
        self.setWindowIcon(QIcon("import/Icon.png"))
        if user_type == "guest":
            self.stacked_widget.setCurrentWidget(self.guest_window)
        elif user_type == "client":
            self.client_window.set_full_name(full_name)
            self.stacked_widget.setCurrentWidget(self.client_window)
        elif user_type == "manager":
            self.manager_window.set_full_name(full_name)
            self.stacked_widget.setCurrentWidget(self.manager_window)
        elif user_type == "admin":
            self.admin_window.set_full_name(full_name)
            self.stacked_widget.setCurrentWidget(self.admin_window)
        else:
            print(f"Неизвестный тип пользователя: {user_type}")


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("")

    if sys.platform == "win32":
        app.setStyle("Windows")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()