from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import json


FILE = Path('books.json')

class Book:
    def __init__(self, id:int, name:str, author:str) -> None:
        self.id = id
        self.name = name
        self.author = author
        pass
    
    def __repr__(self) -> str:
        return f'Book: {self.name} | {self.author}'
    
    def to_dict(self):
        return {'id':self.id, 'name':self.name, 'author':self.author}



app = Flask(__name__)

def get_books() -> list:
    books:list = []
    if FILE.exists():
        with open (FILE, 'r') as f:
            try:
                books = json.load(f)
            except:
                print('CANNOT DECODE')
                
    return books

def set_books(books:list):
    
    with open(FILE, 'w') as f:
        json.dump(books, f, indent=1)

def insert(book:Book):
    books = get_books()
    book.id = len(books) + 1
    books.append(book.to_dict())
    set_books(books)
    print('INSERTED')


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/launch", methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = str(request.form.get('name'))
        book_author = str(request.form.get('author'))
        book = Book(1,book_name,book_author)
        insert(book)
        return redirect(url_for('show_details'))
    return render_template('add_book.html')


@app.route("/details", methods=['GET'])
def show_details():
    books = get_books()
    return render_template('details.html', books = books)


app.run(host="0.0.0.0", port=80)