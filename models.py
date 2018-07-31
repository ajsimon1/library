from app import db

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(255))
    isbn = db.Column(db.String(20), unique=True, index=True)
    date_published = db.Column(db.DateTime())
    title = db.Column(db.String(255), index=True)
    date_added = db.Column(db.DateTime())
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    # returned list from 'fetchall', matches this order

    def __repr__(self):
        return '<Book {} by {}>'.format(self.title, self.author)

class Owner(db.Model):
    __tablename__ = 'owners'
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    books = db.relationship('Book', backref='owners', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
