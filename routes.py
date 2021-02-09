from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>HELLO</h1>'


if __name__ == '__name__':
    app.run()

app.run(port=8000, debug=True)
