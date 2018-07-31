from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ISBNSearchForm(Form):
    isbn = StringField('isbn', validators=[DataRequired()])

class KeywordSearchForm(Form):
    keywords = StringField('keywords', validators=[DataRequired()])
