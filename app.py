from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        'name': 'Green eggs and ham',
        'price': 7.99,
        'isbn': 1756919797,
    },
    {
        'name': 'The cat and the hat',
        'price': 8.99,
        'isbn': 1756919798,
    },
]

@app.route('/books')
def get_books():
    return jsonify({
        'books': books
    })

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price'],
            }

    return jsonify(return_value)


@app.route('/books', methods=['POST'])
def add_book():
    return jsonify(request.get_json())

app.run(port=5000)
