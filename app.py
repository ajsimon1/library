import json
import os
import psycopg2
import requests

from flask import (Flask, render_template, request, flash, redirect,
                    url_for, session)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from forms import BookSearchForm
from dateutil.parser import parse

# TODO configure database for heroku
# TODO you're missing a javascript plugin to dismiss the alerts
# see https://getbootstrap.com/docs/4.0/components/alerts/#dismissing

num = 9780061122910

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# grab environ variables
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('PGUSER')
db_pass = os.environ.get('PGPASSWORD')
db_host = os.environ.get('HOST')


# import models after db instantiation
import models

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BookSearchForm()
    base='https://api.isbndb.com/book/'
    isbn_key = 'o63bZoobFbrynZDVR6fX3mmsRerF0NR4aKwRkJI0'
    headers = {'X-API-KEY': isbn_key}
    if request.method == 'POST':
        if request.form.get('search') == 'Search':
            isbn = str(form.isbn.data)
            try:
                response = requests.get(base+isbn, headers=headers)
                json_resp = json.loads(response.text)
                session['isbndb_results'] = json_resp
                flash('Info for that shit below...', 'info')
                return render_template('index.html', data=json_resp, form=form)
            except:
                flash('There was an issue locating that ISBN...idiot', 'warning')
        elif request.form.get('add') == 'Add':
            pub_date_parsed = parse(session['isbndb_results']['book']['date_published'])
            bad_chars = '[]{}\"\''
            s = str(session['isbndb_results']['book']['authors'])
            auth = "".join(c for c in s if c not in bad_chars)
            book = models.Book(
                author = auth,
                isbn = session['isbndb_results']['book']['isbn13'],
                date_published = pub_date_parsed,
                title = session['isbndb_results']['book']['title'],
            )
            db.session.add(book)
            db.session.commit()
            flash('That shit got added yo...', 'info')
            return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/library')
def library():
    conn = psycopg2.connect(
        dbname = os.environ.get('DB_NAME'),
        password = os.environ.get('PGPASSWORD'),
        user = os.environ.get('PGUSER'),
        host = os.environ.get('HOST'),
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    library = cur.fetchall()
    return render_template('library.html', library=library)

if __name__ == '__main__':
    app.run(debug=True)
