from flask import Flask, render_template, request
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from forms import BookSearchForm
from config import Config
from flask_migrate import Migrate

num = 9781593276041

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BookSearchForm()
    base='https://api.isbndb.com/book/'
    isbn_key = 'o63bZoobFbrynZDVR6fX3mmsRerF0NR4aKwRkJI0'
    headers = {'X-API-KEY': isbn_key}
    if request.method == 'POST':
        isbn = str(form.isbn.data)
        response = requests.get(base+isbn, headers=headers)
        json_resp = json.loads(response.text)
        return render_template('index.html', data=json_resp, form=form)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
