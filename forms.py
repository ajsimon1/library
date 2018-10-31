from flask_wtf import FlaskForm
from flask_wtf.csrf import generate_csrf
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ISBNSearchForm(FlaskForm):
    isbn = StringField('isbn', validators=[DataRequired()])


class AltSearchForm(FlaskForm):
    keywords = StringField('keyword')
    author = StringField('author')

class AddBookManual(FlaskForm):
    # TODO test pinging api in terminal, add approriate fields to form
    title = StringField('title', validators=[DataRequired()])
