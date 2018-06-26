
import json
import requests
import models
import psycopg2

from flask import (Flask, render_template, request, flash, redirect,
                    url_for, session)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from forms import BookSearchForm

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
        if request.form.get('search') == 'Search':
            flash('Info for that shit below...')
            isbn = str(form.isbn.data)
            response = requests.get(base+isbn, headers=headers)
            json_resp = json.loads(response.text)
            session['isbndb_results'] = json_resp
            return render_template('index.html', data=json_resp, form=form)
        elif request.form.get('add') == 'Add':
            book = models.Book(
                author = session['isbndb_results']['book']['authors'],
                isbn = session['isbndb_results']['book']['isbn13'],
                date_published = session['isbndb_results']['book']['date_published'],
                title = session['isbndb_results']['book']['title'],
            )
            db.session.add(book)
            db.session.commit()
            flash('That shit got added yo...')
            return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/library')
def library():
    conn = psycopg2.connect("dbname='library' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    library = cur.fetchall()
    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run(debug=True)
