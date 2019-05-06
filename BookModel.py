from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)

    price = db.Column(db.Float, nullable=False)

    isbn = db.Column(db.Integer)

    def add_book(_name, _price, _isbn):
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()


    def get_all_books():
        return db.session.query(Book).all()


    def get_book(_isbn):
        return db.session.query(Book).filter(Book.isbn == _isbn).first()


    def delete_book(_isbn):
        db.session.query(Book).filter(Book.isbn == _isbn).delete()
        db.session.commit()


    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }

        return json.dumps(book_object)
