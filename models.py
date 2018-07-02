from app import db

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(255))
    isbn = db.Column(db.String(20), unique=True, index=True)
    date_published = db.Column(db.DateTime())
    title = db.Column(db.String(255), index=True)
    # returned list from 'fetchall', matches this order

    def __repr__(self):
        return '<Book {} by {}>'.format(self.title, self.author)
