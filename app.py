from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error

DB_NAME = "smile.db"

app = Flask(__name__)
app.secret_key = "banana"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def render_homepage():
    return render_template('Home.html', logged_in=is_logged_in())


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

    return render_template('Menu.html', products=product_list, logged_in=is_logged_in())


@app.route('/Contact')
def render_contact_page():
    return render_template('Contact.html', logged_in=is_logged_in())


@app.route('/Login', methods=["GET", "POST"])
def render_login_page():
    if is_logged_in():
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        query = """SELECT id, fname, password FROM customer WHERE email = ?"""
        con = create_connection(DB_NAME)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            userid = user_data[0][0]
            firstname = user_data[0][1]
            db_password = user_data[0][2]
        except IndexEror:
            return redirect('/Login?error=Email+invalid+or+password+incorrect')

        if db_password != password:
            return redirect('/Login?error=Email+invalid+or+password+incorrect')

        session['email'] = email
        session['userid'] = userid
        session['firstname'] = firstname
        print(session)
        return redirect('/')
    return render_template('login.html', logged_in=is_logged_in())


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if is_logged_in():
        return redirect('/')

    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').strip().title()
        lname = request.form.get('lname').strip().title()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return redirect('/signup?error=Passwords+dont+match')

        if len(password) < 8:
            return redirect('/signup?error=Password+must+be+8+character+or+more')

        con = create_connection(DB_NAME)

        query = "INSERT INTO customer(id, fname, lname, email, password) VALUES(NULL,?,?,?,?)"

        cur = con.cursor()

        try:
            cur.execute(query, (fname, lname, email, password))
        except sqlite3.IntergrityError:
            return redirect('/signup?error=email+is+already+used')

        con.commit()
        con.close()
        return redirect('/Login')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/?message=s=you+have+logged+out')


def is_logged_in():
    if session.get('email') is None:
        print("not logged in")
        return False
    else:
        print("logged in")
        return True


app.run(host='0.0.0.0')
