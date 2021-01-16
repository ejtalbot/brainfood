from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Grocery(Base):
    __tablename__ = 'grocery'
    grocery_id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship("Category", back_populates="groceries")
    date_bought = Column(DateTime, default=datetime.utcnow)
    date_finished = Column(DateTime)

    def __init__(self, name=None, count=None, category_id=None):
        self.name = name
        self.count = count
        self.category_id = category_id
        #self.date_bought = datetime.utcnow()


class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    groceries = relationship("Grocery", back_populates="category") 

    def __init__(self, name):
        self.name = name
