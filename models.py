from app import db

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
