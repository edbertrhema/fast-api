from sqlalchemy import Column,String,Integer,Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP 
from sqlalchemy.sql import func
from .database import Base

class Products(Base):
    __tablename__ = "products"

    id =  Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    is_sale = Column(Boolean, default=True)
    inventory = Column(Integer, server_default=(str(10)))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False)

    buyer = Relationship("Users")

class Users(Base):
    __tablename__ = "users"
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    phone_number = Column(String)

class Favorites(Base):
    __tablename__ = "favorites"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
