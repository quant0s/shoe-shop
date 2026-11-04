from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role = Column(String(30), nullable=False)
    full_name = Column(String(30), nullable=False)
    login = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)


class Items(Base):
    __tablename__ = 'items'

    item_number = Column(String(30), primary_key=True)
    name = Column(String(30), nullable=False)
    unit_measurement = Column(String(30), nullable=False)
    cost = Column(Integer, nullable=False)
    provider = Column(String(30), nullable=False)
    manufacturer = Column(String(30), nullable=False)
    item_category = Column(String(30), nullable=False)
    current_discount = Column(Integer, nullable=False)
    quantity_stock = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)
    photo = Column(String(30), default='picture.png')


class PickupPoints(Base):
    __tablename__ = 'pickup_points'

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)


class Orders(Base):
    __tablename__ = 'orders'

    order_number = Column(Integer, primary_key=True)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)
    receipt_code = Column(Integer, nullable=False)
    order_status = Column(String(30), nullable=False)
    id_pickup_point = Column(Integer, ForeignKey('pickup_points.id', onupdate='RESTRICT', ondelete='RESTRICT'))
    id_user = Column(Integer, ForeignKey('users.id', onupdate='RESTRICT', ondelete='RESTRICT'))


class OrdersItems(Base):
    __tablename__ = 'orders_items'

    order_number = Column(Integer, ForeignKey('orders.order_number', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
    item_number = Column(String(30), ForeignKey('items.item_number', onupdate='RESTRICT', ondelete='RESTRICT'), primary_key=True)
    quantity = Column(Integer)


if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:p@ssw0rd@localhost:5432/shoe_shop')

    Base.metadata.create_all(engine)

    print('Все успешно добавлено')