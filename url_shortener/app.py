from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'


db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(50), unique = True, nullable = False)
    url = db.Column(db.String(100), nullable = False)
    
    def __init__(self, key, url):
        self.key = key
        self.url = url
    
    def __repr__(self) -> str:
        return f'{self.key} -> {self.url}'

def generate_key(length = 5):
    characters = string.ascii_letters + string.digits
    
    while True:
        key = ''.join(random.choices(characters, k = length))
        if not Url.query.filter_by(key = key).first():
            return key
    
    

@app.route('/', methods = ['GET', 'POST'])
def add_url():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        short_code = generate_key()
        
        new_url = Url(key = short_code, url = long_url)
        
        db.session.add(new_url)
        db.session.commit()
        
        return render_template('index.html', short_url = f'https://abc.xyz/{short_code}')
    
    return render_template('index.html')

@app.route('/redirect_orig', methods=['POST'])
def redirect_to_orig():
    short_url:str = str(request.form.get('short_url'))
    short_code = short_url.rsplit('/', 1)[-1]
    url_entry = Url.query.filter_by(key=short_code).first()
    if url_entry:
        return redirect(url_entry.url)
    else:
        return "URL not found", 404

@app.route('/show_urls')
def display_all():
    try:
        urls = Url.query.all()
        return render_template('display.html', urls = urls)
    
    except Exception as e:
        return render_template('display.html', urls = None)

if __name__ == '__main__':
    app.run()