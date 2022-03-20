from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error

DB_NAME = "smile.db"

app = Flask(__name__)


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def render_homepage():
    return render_template('Home.html')


@app.route('/Menu')
def render_menu_page():

    # connect to database
    con = create_connection(DB_NAME)

    # select the things you want from the table
    query = 'SELECT name, description, volume, price, image FROM product'

    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()

    return render_template('Menu.html', products=product_list)


@app.route('/Contact')
def render_contact_page():
    return render_template('Contact.html')


@app.route('/Login')
def render_login_page():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    print(request.form)
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    con = create_connection(DB_NAME)

    query = "INSERT INTO customer(id, fname, lname, email, password) VALUES(NULL,?,?,?,?)"

    cur = con.cursor()
    cur.execute(query, (fname, lname, email, password))
    con.commit()
    con.close()

    return render_template('signup.html')


app.run(host='0.0.0.0')
