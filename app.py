from flask import Flask, jsonify, request, Response
import json

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


def validBookObject(bookObject):
    return "name" in bookObject and "price" in bookObject and "isbn" in bookObject


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()

    if validBookObject(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)

        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Correct data should be passed in"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


def valid_put_request_data(bookObject):
    return "name" in bookObject and "price" in bookObject


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()

    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Correct data should be passed in"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }

    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            books[i] = new_book

    response = Response("", status=204, mimetype='application/json')
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()

    updated_book = {}
    if 'name' in request_data:
        updated_book['name'] = request_data['name']
    if 'price' in request_data:
        updated_book['price'] = request_data['price']

    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)

    response = Response("", status=204, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response("", status=204, mimetype='application/json')
            return response

    invalidBookObjectErrorMsg = {
        "error": "A book with that ISBN was not found"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response


app.run(port=5000)
