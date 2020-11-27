from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    lang = Column(String(10))
    address = Column(String(100))
    phone_number = Column(String(100))

    query: sql.Select
