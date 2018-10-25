from flask_wtf import Form
from flask_wtf.csrf import generate_csrf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ISBNSearchForm(Form):
    isbn = StringField('isbn', validators=[DataRequired()])


class KeywordSearchForm(Form):
    keywords = StringField('keyword')
    author = StringField('author')

class AddBookManual(Form):
    # TODO test pinging api in terminal, add approriate fields to form
    title = StringField('title', validators=[DataRequired()])
