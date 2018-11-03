from flask_wtf import FlaskForm
from flask_wtf.csrf import generate_csrf
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

class ISBNSearchForm(FlaskForm):
    isbn = StringField('isbn', validators=[DataRequired()])


class AltSearchForm(FlaskForm):
    keywords = StringField('keyword')
    author = StringField('author')

class AddBookForm(FlaskForm):
    # TODO test pinging api in terminal, add approriate fields to form
    author = StringField('author', validators=[DataRequired()])
    isbn = StringField('isbn', validators=[DataRequired()])
    date_published = DateField('date_pub')
    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('add_book_submit')
