from flask import Flask, jsonify

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
def hello_world():
    return jsonify({
        'books': books
    })

app.run(port=5000)
