from flask import Flask, jsonify, request, Response
import json

from settings import app
from Book import (
    get_all_books,
    add_book,
    replace_book,
)


@app.route('/books')
def get_books():
    return jsonify({
        'books': get_all_books()
    })

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = get_book(isbn)

    return jsonify(return_value)


def validBookObject(bookObject):
    return "name" in bookObject and "price" in bookObject and "isbn" in bookObject


@app.route('/books', methods=['POST'])
def create_book():
    request_data = request.get_json()

    if validBookObject(request_data):
        add_book(request_data['name'], request_data['price'], request_data['isbn'])

        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
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
def put_book(isbn):
    request_data = request.get_json()

    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Correct data should be passed in"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    replace_book(isbn, request_data['name'], request_data['price'])

    response = Response("", status=204, mimetype='application/json')
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
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
