from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
<<<<<<< HEAD
    return '<h1>This is only the beginning....<h1>'
=======
    return '<h1>This is only the beginning<h1>'
>>>>>>> origin/main

app.run(host='0.0.0.0')