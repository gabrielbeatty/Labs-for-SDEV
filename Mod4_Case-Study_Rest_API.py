#Gabriel Beatty
#SDEV 220
#Module 4 Lab-Case Study: Python APIs


from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Book Model inheriting from db.Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """Helper to convert object to dictionary for JSON responses"""
        return {
            "id": self.id,
            "book_name": self.book_name,
            "author": self.author,
            "publisher": self.publisher
        }

# Initialize the database tables
with app.app_context():
    db.create_all()

# Create the CRUD endpoints

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(new_book)  
    db.session.commit()       
    # Save to database
    return jsonify(new_book.to_dict()), 201

@app.route('/books', methods=['GET'])
def get_all_books():
    all_books = Book.query.all() 
    return jsonify([book.to_dict() for book in all_books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)  
    # Returns 404 if not found
    return jsonify(book.to_dict())

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    
    book.book_name = data.get('book_name', book.book_name)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)
    
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)