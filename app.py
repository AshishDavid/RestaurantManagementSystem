from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin123'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('resto.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/register')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO accounts (username, email, lastname, firstname, password, enabled) VALUES (%s, %s, %s, %s, %s)", (username, email, lastname, firstname, hash_password))
        account = cursor.commit()
        session['name'] = username
        session['email'] = email
        return redirect(url_for("home"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


if __name__ == '__main__':
    app.run()
