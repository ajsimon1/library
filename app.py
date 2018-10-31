import json
import os
import psycopg2
import requests

from flask import (Flask, render_template, request, flash, redirect,
                    url_for, session)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from forms import ISBNSearchForm, AltSearchForm
from dateutil.parser import parse

# TODO configure database for heroku
# TODO you're missing a javascript plugin to dismiss the alerts
# see https://getbootstrap.com/docs/4.0/components/alerts/#dismissing
# note if pipfile out of date run pipenv lock in cmd, commit and push

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
    isbn_form = ISBNSearchForm()
    alt_form = AltSearchForm()
    base_book='https://api.isbndb.com/book/'
    base_kw='https://api.isbndb.com/books/'
    base_auth='https://api.isbndb.com/author/'
    isbn_key = 'o63bZoobFbrynZDVR6fX3mmsRerF0NR4aKwRkJI0'
    headers = {'X-API-KEY': isbn_key}
    max_return='?pageSize=25'
    if request.method == 'POST':
        if request.form.get('search') == 'Search':
            isbn = str(request.form['isbn'])
            response = requests.get(base_book+isbn, headers=headers)
            json_resp = json.loads(response.text)
            session['isbndb_results'] = json_resp
            if 'errorMessage' in json_resp:
                flash('There was an issue locating that ISBN...idiot', 'warning')
            else:
                flash('Info for that shit below...', 'info')
                return render_template('index.html',
                                       data=json_resp,
                                       isbn_form=isbn_form,
                                       alt_form=alt_form)
        elif request.form.get('alt-search') == 'Alt-Search':
            signal = ''
            if alt_form.keywords.data:
                kw = str(alt_form.keywords.data)
                response = requests.get(base_kw+kw+max_return, headers=headers)
                json_resp = json.loads(response.text)
                print(json_resp)
                session['isbndb_results'] = json_resp
                signal='kw'
                if 'errorMessage' in json_resp:
                    flash('The keyword there was shit, no returned results', 'warning')
                else:
                    flash('I got you baby...', 'info')
            elif alt_form.author.data:
                auth = str(alt_form.author.data)
                response = requests.get(base_auth+auth+max_return, headers=headers)
                json_resp = json.loads(response.text)
                print(json_resp)
                session['isbndb_results'] = json_resp
                signal='author'
                if 'errorMessage' in json_resp:
                    flash('Don"t know that guy, or gal', 'warning')
                else:
                    flash('There he/she is', 'info')
            return render_template('index.html',
                                   data=json_resp,
                                   alt_form=alt_form,
                                   isbn_form=isbn_form,
                                   signal=signal)

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
    return render_template('index.html',
                            isbn_form=isbn_form,
                            alt_form=alt_form,
                            signal=None)

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

@app.route('/add_book')
def add_book():
    # TODO finish this template
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
