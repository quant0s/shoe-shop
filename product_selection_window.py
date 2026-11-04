import sys
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QSpinBox, QMessageBox, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
import psycopg


class ProductSelectionWindow(QDialog):
    """Окно выбора товаров для заказа"""

    items_selected = Signal(str)  # Сигнал с выбранными товарами в формате "артикул#количество,артикул#количество"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор товаров для заказа")
        self.setMinimumSize(900, 700)
        self.setWindowIcon(QIcon("import/Icon.png") if parent else None)

        self.selected_items = []  # [(item_number, name, quantity), ...]
        self.products_data = []  # Кэш данных товаров

        self.setup_ui()
        self.load_products()

        # Настройка стилей
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-family: 'Times New Roman';
                font-size: 12px;
            }
            QPushButton {
                background-color: #7FFF00;
                color: black;
                border: 1px solid #5FCC00;
                border-radius: 4px;
                padding: 8px 16px;
                font-family: 'Times New Roman';
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00FA9A;
            }
            QPushButton:pressed {
                background-color: #7FFF00;
            }
            QTableWidget {
                gridline-color: #ddd;
                font-family: 'Times New Roman';
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 6px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            QSpinBox {
                padding: 3px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Заголовок
        title_label = QLabel("Доступные товары (с остатком на складе)")
        title_font = QFont("Times New Roman", 14, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Таблица доступных товаров
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "✓", "Артикул", "Название", "Категория", "Цена, ₽", "В наличии", "Кол-во"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)

        # Кнопки для таблицы товаров
        table_buttons_layout = QHBoxLayout()

        self.select_all_btn = QPushButton("Выбрать всё")
        self.select_all_btn.clicked.connect(self.select_all_items)
        table_buttons_layout.addWidget(self.select_all_btn)

        self.deselect_all_btn = QPushButton("Снять всё")
        self.deselect_all_btn.clicked.connect(self.deselect_all_items)
        table_buttons_layout.addWidget(self.deselect_all_btn)

        self.add_selected_btn = QPushButton("Добавить выбранные в заказ")
        self.add_selected_btn.clicked.connect(self.add_selected_items)
        table_buttons_layout.addWidget(self.add_selected_btn)

        table_buttons_layout.addStretch()
        layout.addLayout(table_buttons_layout)

        # Разделитель
        separator = QLabel("────────────────────────────────────────")
        separator.setAlignment(Qt.AlignCenter)
        layout.addWidget(separator)

        # Заголовок для выбранных товаров
        selected_title = QLabel("Товары в заказе:")
        selected_font = QFont("Times New Roman", 12, QFont.Bold)
        selected_title.setFont(selected_font)
        layout.addWidget(selected_title)

        # Таблица выбранных товаров
        self.selected_table = QTableWidget()
        self.selected_table.setColumnCount(5)
        self.selected_table.setHorizontalHeaderLabels([
            "Артикул", "Название", "Количество", "Сумма, ₽", "Удалить"
        ])
        self.selected_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.selected_table.setAlternatingRowColors(True)
        layout.addWidget(self.selected_table, 1)

        # Итоговая сумма
        self.total_label = QLabel("Итого: 0.00 ₽")
        self.total_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        layout.addWidget(self.total_label)

        # Кнопки подтверждения/отмены
        dialog_buttons = QHBoxLayout()
        dialog_buttons.addStretch()

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        dialog_buttons.addWidget(self.cancel_btn)

        self.ok_btn = QPushButton("Сохранить выбор")
        self.ok_btn.clicked.connect(self.save_selection)
        dialog_buttons.addWidget(self.ok_btn)

        layout.addLayout(dialog_buttons)

    def load_products(self):
        try:
            conn = psycopg.connect(
                host="localhost",
                dbname="shoe_shop",
                port="5432",
                user="postgres",
                password="p@ssw0rd"
            )
            cursor = conn.cursor()

            cursor.execute("""
                SELECT item_number, name, item_category, cost, 
                       current_discount, quantity_stock, manufacturer
                FROM items 
                WHERE quantity_stock > 0 
                ORDER BY name
            """)

            self.products_data = cursor.fetchall()
            self.table.setRowCount(len(self.products_data))

            for row, product in enumerate(self.products_data):
                item_number, name, category, cost, discount, quantity, manufacturer = product

                # Чекбокс выбора
                checkbox_item = QTableWidgetItem()
                checkbox_item.setCheckState(Qt.Unchecked)
                checkbox_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 0, checkbox_item)

                # Артикул
                self.table.setItem(row, 1, QTableWidgetItem(str(item_number)))

                # Название с производителем
                name_with_manufacturer = f"{name} ({manufacturer})" if manufacturer else name
                name_item = QTableWidgetItem(name_with_manufacturer)
                name_item.setToolTip(name_with_manufacturer)
                self.table.setItem(row, 2, name_item)

                # Категория
                self.table.setItem(row, 3, QTableWidgetItem(str(category)))

                # Цена со скидкой
                final_price = cost * (1 - discount / 100)
                price_text = f"{final_price:.2f}"
                if discount > 0:
                    price_text = f"<s>{cost:.2f}</s> {final_price:.2f}"
                    price_item = QTableWidgetItem()
                    price_item.setData(Qt.DisplayRole, f"{final_price:.2f}")
                    if discount > 15:
                        price_item.setForeground(Qt.red)
                else:
                    price_item = QTableWidgetItem(price_text)

                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 4, price_item)

                # Количество на складе
                stock_item = QTableWidgetItem(str(quantity))
                stock_item.setTextAlignment(Qt.AlignCenter)
                if quantity < 10:
                    stock_item.setForeground(Qt.red)
                self.table.setItem(row, 5, stock_item)

                # SpinBox для выбора количества
                spinbox = QSpinBox()
                spinbox.setMinimum(1)
                spinbox.setMaximum(quantity)
                spinbox.setValue(1)
                spinbox.valueChanged.connect(self.update_spinbox_max)
                self.table.setCellWidget(row, 6, spinbox)

            cursor.close()
            conn.close()

            self.table.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров: {str(e)}")

    def update_spinbox_max(self):
        """Обновляет максимальное значение спинбокса"""
        pass

    def select_all_items(self):
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.Checked)

    def deselect_all_items(self):
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.Unchecked)

    def add_selected_items(self):
        items_added = False

        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                item_number = self.table.item(row, 1).text()
                name = self.table.item(row, 2).text()

                # Получаем цену
                price_item = self.table.item(row, 4)
                price_text = price_item.data(Qt.DisplayRole) if price_item else "0"
                try:
                    price = float(price_text.replace('<s>', '').replace('</s>', '').split()[-1])
                except:
                    price = 0.0

                spinbox = self.table.cellWidget(row, 6)
                quantity = spinbox.value() if spinbox else 1

                # Проверяем, не добавлен ли уже этот товар
                existing_index = -1
                for i, (existing_id, _, existing_qty) in enumerate(self.selected_items):
                    if existing_id == item_number:
                        existing_index = i
                        break

                if existing_index >= 0:
                    # Обновляем количество существующего товара
                    old_qty = self.selected_items[existing_index][2]
                    new_qty = old_qty + quantity

                    # Проверяем доступность на складе
                    stock_item = self.table.item(row, 5)
                    max_qty = int(stock_item.text()) if stock_item else 0

                    if new_qty <= max_qty:
                        self.selected_items[existing_index] = (item_number, name, new_qty)

                        # Обновляем строку в таблице
                        self.selected_table.item(existing_index, 2).setText(str(new_qty))
                        total = price * new_qty
                        self.selected_table.item(existing_index, 3).setText(f"{total:.2f}")
                    else:
                        QMessageBox.warning(self, "Ошибка",
                                            f"Нельзя добавить {quantity} шт. товара '{name}'\n"
                                            f"Максимально доступно: {max_qty} шт.")
                else:
                    # Добавляем новый товар
                    self.selected_items.append((item_number, name, quantity))

                    # Добавляем в таблицу выбранных
                    row_pos = self.selected_table.rowCount()
                    self.selected_table.insertRow(row_pos)

                    # Артикул
                    id_item = QTableWidgetItem(item_number)
                    self.selected_table.setItem(row_pos, 0, id_item)

                    # Название
                    name_item = QTableWidgetItem(name)
                    self.selected_table.setItem(row_pos, 1, name_item)

                    # Количество
                    qty_item = QTableWidgetItem(str(quantity))
                    qty_item.setTextAlignment(Qt.AlignCenter)
                    self.selected_table.setItem(row_pos, 2, qty_item)

                    # Сумма
                    total = price * quantity
                    total_item = QTableWidgetItem(f"{total:.2f}")
                    total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.selected_table.setItem(row_pos, 3, total_item)

                    # Кнопка удаления
                    remove_btn = QPushButton("✕")
                    remove_btn.setToolTip("Удалить товар из заказа")
                    remove_btn.setFixedSize(30, 25)
                    remove_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #7FFF00;
                            color: black;
                            border-radius: 3px;
                            font-weight: bold;
                            border: 1px solid #5FCC00;
                        }
                        QPushButton:hover {
                            background-color: #6EEF00;
                        }
                        QPushButton:pressed {
                            background-color: #5EDF00;
                        }
                    """)
                    remove_btn.clicked.connect(lambda checked, r=row_pos: self.remove_selected_item(r))
                    self.selected_table.setCellWidget(row_pos, 4, remove_btn)

                # Снимаем выделение
                checkbox_item.setCheckState(Qt.Unchecked)
                items_added = True

        if items_added:
            self.update_total()

    def remove_selected_item(self, row):
        if 0 <= row < len(self.selected_items):
            self.selected_items.pop(row)
            self.selected_table.removeRow(row)
            self.update_total()

    def update_total(self):
        total = 0.0
        for row in range(self.selected_table.rowCount()):
            total_item = self.selected_table.item(row, 3)
            if total_item:
                try:
                    total += float(total_item.text())
                except:
                    pass

        self.total_label.setText(f"Итого: {total:.2f} ₽")

    def save_selection(self):
        if not self.selected_items:
            QMessageBox.warning(self, "Внимание", "Не выбрано ни одного товара")
            return

        self.accept()

    def get_selected_items_string(self):
        """Возвращает строку артикулов в формате item1#qty1,item2#qty2,..."""
        if not self.selected_items:
            return ""

        result_parts = []
        for item_number, _, quantity in self.selected_items:
            result_parts.append(f"{item_number}#{quantity}")

        return ",".join(result_parts)