from flask import Flask, jsonify, request, Response
import json
import jwt
import datetime as dt

from settings import app
from BookModel import *
from UserModel import User

app.config['SECRET_KEY'] = 'hello'


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = dt.datetime.utcnow() + dt.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', status=401, mimetype='application/json')


@app.route('/books')
def get_books():
    token = request.args.get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({'error': 'Need a valid token to view this page.'}), 401
    return jsonify({
        'books': Book.get_all_books()
    })

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)

    return jsonify(return_value)


def validBookObject(bookObject):
    return "name" in bookObject and "price" in bookObject and "isbn" in bookObject


@app.route('/books', methods=['POST'])
def create_book():
    request_data = request.get_json()

    if validBookObject(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])

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

    Book.replace_book(isbn, request_data['name'], request_data['price'])

    response = Response("", status=204, mimetype='application/json')
    return response


@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
    request_data = request.get_json()

    updated_book = {}
    if 'name' in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if 'price' in request_data:
        Book.update_book_price(isbn, request_data['price'])

    response = Response("", status=204, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204, mimetype='application/json')
        return response
    invalidBookObjectErrorMsg = {
        "error": "A book with that ISBN was not found"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response


app.run(port=5000)
