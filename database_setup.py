import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, DateTime, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(250), nullable=False, unique=True)
    items = relationship('Item', backref='category', lazy='select')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
        }


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(80), nullable=False)
    description = Column(String(250))
    username = Column(String(250))
    # image = Column(Binary)
    create_ts = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    __table_args__ = (UniqueConstraint('category_id', 'item_name'),)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'item_id': self.item_id,
            'category_id': self.category_id,
            'item_name': self.item_name,
            'description': self.description
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
