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


@app.route('/Home')
def render_homepage():
    return render_template('home.html')


@app.route('/Menu')
def render_menu_page():

    # connect to database
    con = create_connection(DB_NAME)

    # select the things you want from the table
    query = 'SELECT name, description, volume, price, image FROM products'

    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()

    return render_template('menu.html', products=product_list)


@app.route('/Contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0')
