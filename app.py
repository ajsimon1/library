from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    base='https://api.isbndb.com/book/'
    isbn_key = 'o63bZoobFbrynZDVR6fX3mmsRerF0NR4aKwRkJI0'
    headers = {'X-API-KEY': isbn_key}
    if request.method == 'POST':
        isbn = request.form['isbn-input']
        response = requests.get(base+isbn, headers=headers)
        json_resp = json.loads(response.text)
        render_template('index.html', response=json_resp)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
