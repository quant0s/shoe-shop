import openpyxl
from sqlalchemy import create_engine, text


def parse_articles(articles_str):
    if articles_str is None or str(articles_str).strip() == '':
        return []

    articles_str = str(articles_str).strip()

    if articles_str.startswith("'") and articles_str.endswith("'"):
        articles_str = articles_str[1:-1]

    parts = [part.strip() for part in articles_str.split(',')]
    articles_data = []

    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            article = parts[i]
            try:
                quantity = int(parts[i + 1])
                articles_data.append((article, quantity))
            except ValueError:
                continue

    return articles_data


def import_items(excel_file_path, db_connection_string):
    engine = create_engine(db_connection_string)

    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    print("Импорт данных...")

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for row_num in range(2, sheet.max_row + 1):
                article = sheet.cell(row=row_num, column=1).value
                name = sheet.cell(row=row_num, column=2).value
                measurement = sheet.cell(row=row_num, column=3).value
                cost = sheet.cell(row=row_num, column=4).value
                provider = sheet.cell(row=row_num, column=5).value
                manufacterer = sheet.cell(row=row_num, column=6).value
                category = sheet.cell(row=row_num, column=7).value
                discount = sheet.cell(row=row_num, column=8).value
                count = sheet.cell(row=row_num, column=9).value
                description = sheet.cell(row=row_num, column=10).value
                photo = sheet.cell(row=row_num, column=11).value

                if article is None:
                    break
                query = text("""
                             INSERT INTO items (item_number, name, unit_measurement,
                                                       cost, provider, manufacturer, item_category, current_discount,
                                                       quantity_stock, description, photo)
                             VALUES (:item_number, :name, :unit_measurement, :cost, :provider, :manufacturer, :item_category,
                                 :current_discount, :quantity_stock, :description, :photo)
                             """)

                conn.execute(query, {
                    'item_number': str(article),
                    'name': str(name),
                    'unit_measurement': str(measurement),
                    'cost': int(cost),
                    'provider': str(provider),
                    'manufacturer': str(manufacterer),
                    'item_category': str(category),
                    'current_discount': int(discount),
                    'quantity_stock': int(count),
                    'description': str(description),
                    'photo': str(photo) if str(photo) else None
                })
            trans.commit()
        except Exception as e:
            print(f"Ошибка: {e}")
            trans.rollback()
            raise

        finally:
            workbook.close()


def import_users(excel_file_path, db_connection_string):
    engine = create_engine(db_connection_string)

    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    print("Импорт данных...")

    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        try:
            for row_num in range(2, sheet.max_row + 1):
                role = sheet.cell(row=row_num, column=1).value
                full_name = sheet.cell(row=row_num, column=2).value
                login = sheet.cell(row=row_num, column=3).value
                password = sheet.cell(row=row_num, column=4).value

                if role is None:
                    break
                query = text("""
                             INSERT INTO users (role, full_name, login, password)
                             VALUES (:role, :full_name, :login, :password)
                             """)

                conn.execute(query, {
                    'role': str(role),
                    'full_name': str(full_name),
                    'login': str(login),
                    'password': str(password)
                })
            trans.commit()
        except Exception as e:
            print(f"Ошибка: {e}")
            trans.rollback()
            raise

        finally:
            workbook.close()



def import_pickup_points(excel_file_path, db_connection_string):
    engine = create_engine(db_connection_string)

    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    print("Импорт данных...")

    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(text("ALTER SEQUENCE pickup_points_id_seq RESTART WITH 1"))
        try:
            for row_num in range(1, sheet.max_row + 1):
                address = sheet.cell(row=row_num, column=1).value

                if address is None:
                    break
                query = text("""
                             INSERT INTO pickup_points (address)
                             VALUES (:address)
                             """)

                conn.execute(query, {
                    'address': str(address),
                })
            trans.commit()
        except Exception as e:
            print(f"Ошибка: {e}")
            trans.rollback()
            raise

        finally:
            workbook.close()


def import_orders(excel_file_path, db_connection_string):
    engine = create_engine(db_connection_string)

    print("Импорт данных...")

    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(text("ALTER SEQUENCE orders_order_number_seq RESTART WITH 1"))
        result = conn.execute(text("SELECT id, full_name FROM users"))
        user_mapping = {row.full_name: row.id for row in result}

        workbook = openpyxl.load_workbook(excel_file_path)
        sheet = workbook.active

        try:
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] is None:
                    break;

                user_name = str(row[5]) if row[5] else ""
                user_id = user_mapping.get(user_name)

                articles_data = parse_articles(row[1])
                order_date = row[2].date()
                delivery_date = row[3].date()

                order_query = text("""
                                   INSERT INTO orders (order_number, order_date, delivery_date, id_pickup_point,
                                                       id_user, receipt_code, order_status)
                                   VALUES (:order_number, :order_date, :delivery_date, :id_pickup_point, :id_user,
                                           :receipt_code, :order_status)
                                   """)

                conn.execute(order_query, {
                    'order_number': int(row[0]),
                    'order_date': order_date,
                    'delivery_date': delivery_date,
                    'id_pickup_point': int(row[4]),
                    'id_user': user_id,
                    'receipt_code': int(row[6]),
                    'order_status': str(row[7])
                })

                for article, quantity in articles_data:
                    item_query = text("""
                                      INSERT INTO orders_items (order_number, item_number, quantity)
                                      VALUES (:order_number, :item_number, :quantity)
                                      """)

                    conn.execute(item_query, {
                        'order_number': int(row[0]),
                        'item_number': article,
                        'quantity': quantity
                    })
            trans.commit()
        except Exception as e:
            print(f"Ошибка при импорте: {e}")
            trans.rollback()
            raise

        finally:
            workbook.close()


import_items('import/Tovar.xlsx', 'postgresql://postgres:p%40ssw0rd@localhost:5432/shoe_shop')
import_users('import/user_import.xlsx', 'postgresql://postgres:p%40ssw0rd@localhost:5432/shoe_shop')
import_pickup_points('import/Пункты выдачи_import.xlsx', 'postgresql://postgres:p%40ssw0rd@localhost:5432/shoe_shop')
import_orders('import/Заказ_import.xlsx', 'postgresql://postgres:p%40ssw0rd@localhost:5432/shoe_shop')