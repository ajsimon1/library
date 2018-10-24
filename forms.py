from flask_wtf import Form
from flask_wtf.csrf import generate_csrf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ISBNSearchForm(Form):
    isbn = StringField('isbn', validators=[DataRequired()])


class KeywordSearchForm(Form):
    keywords = StringField('keywords', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    # alt_search_csrf = generate_csrf()
    # TODO add other fields to search by
    # TODO update name of form to alternate search or something

class AddBookManual(Form):
    # TODO test pinging api in terminal, add approriate fields to form
    title = StringField('title', validators=[DataRequired()])
