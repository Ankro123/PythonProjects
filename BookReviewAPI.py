from flask import Flask, request, jsonify
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
    try:
        if FILE.exists():
            with open (FILE, 'r') as f:
                return json.load(f)
    except Exception:
                print('CANNOT DECODE')
    return []

def set_books(books:list):
    
    with open(FILE, 'w') as f:
        json.dump(books, f, indent=1)

def insert(book:Book):
    books = get_books()
    book.id = len(books) + 1

    books.append(book.to_dict())
    set_books(books)

def update(book_data, id):
    books:list = get_books()
    
    for book in books:
        if book['id'] == id:
            book['name'] = book_data.get('name', book['name'])
            book['author'] = book_data.get('author', book['author'])
            set_books(books)
            return True, book
        
    return False, None

@app.route("/api/books", methods=['POST'])
def add_book():
    try:
        book_details = request.get_json()
        
        if not book_details.get('name') or not book_details.get('author'):
            return jsonify({"error": "Missing 'author' or 'name'"}), 400
        
        book_name = book_details['name']
        book_author = book_details['author']
        
        book = Book(1,book_name,book_author)
        
        insert(book)
        return jsonify({"message": "Book Added", "book": book.to_dict()}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/books/<int:id>", methods=['PUT'])
def update_book(id):
    book_data = request.get_json()
    
    flag, book = update(book_data, id)
    
    if flag:
        return jsonify({"message":"BOOK UPDATED", "book":book}), 200
    else:
        return jsonify({"error":"Book Not Found!"}), 404
        

@app.route("/api/books", methods=['GET'])
def show_details():
    books = get_books()
    return jsonify({"message": "BOOK DETAILS", "books": books})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)