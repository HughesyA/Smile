from flask import Flask, render_template
app = Flask(__name__)

@app.route('/Home')
def render_homepage():
    return render_template('home.html')

@app.route('/Menu')
def render_menu_page():
    return render_template('menu.html')

@app.route('/Contact')
def render_Contact_page():
    return render_template('contact.html')

app.run(host='0.0.0.0')