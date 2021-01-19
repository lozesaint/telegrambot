from utils.db_api.database import db
from sqlalchemy import (Column, Integer, BigInteger, Sequence,
                        String, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    feedback = Column(String(250))
    phone_number = Column(String(20))
    address = Column(String(150))
    query: sql.Select


class Item(db.Model):
    __tablename__ = "items"
    query: sql.select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)

    category_code = Column(String(20))
    category_name = Column(String(50))

    name = Column(String(250))
    photo = Column(String(250))
    available_sizes = Column(String(20))
    active = Column(Boolean, default=True)
    price = Column(String(20))

    def __repr__(self):
        return f"""
Item #{self.id} - {self.name}
Category: {self.category_name}
Sizes: {self.available_sizes}
Price: {self.price}
"""


class Purchase(db.Model):
    __tablename__ = "purchases"
    query: sql.Select
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    amount = Column(Integer)
    quantity = Column(Integer)
    purchase_time = Column(TIMESTAMP)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    email = Column(String(200))
    receiver = Column(String(100))
    successful = Column(Boolean, default=False)


class Cart(db.Model):
    __tablename__ = 'Cart'
    query: sql.Select
    id = Column(Integer, Sequence("cart_id_seq"), primary_key=True)
    item_id = Column(String(10))
    chat_id = Column(BigInteger)
    size = Column(String(5))
    quantity = Column(Integer)


class Order(db.Model):
    __tablename__ = 'Order'
    query: sql.Select
    id = Column(Integer, Sequence("order_id_seq"), primary_key=True)
    item_ids = Column(String(512))
    sum = Column(Integer)
    is_cash = Column(Boolean, default=False)
    status = Column(Integer)
