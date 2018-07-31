from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class BookSearchForm(Form):
    isbn = StringField('isbn', validators=[DataRequired()])
