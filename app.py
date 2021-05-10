import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'monica'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

app.secret_key = 'pmir@7est'


@app.route('/')
def home():
    return render_template('resto.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        password = request.form['password'].encode('utf-8')
        telephone = request.form['telephone']
        address = request.form['address']
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO accounts (username,password, email, firstname, lastname, address, telephone, accountType, enabled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (username, hash_password, email, firstname, lastname, address, telephone, 1, True))
        mysql.connection.commit()
        session['name'] = username
        session['email'] = email

        return redirect(url_for("home"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s OR email = % s',
                       (username, username))
        account = cursor.fetchone()
        if account:
            if bcrypt.hashpw(password, account['password'].encode('utf-8')) == account['password'].encode('utf-8'):
                session['name'] = username
                return render_template('resto.html')
            else:
                msg = 'Incorrect password !'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Incorrect username / email !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('resto.html')


if __name__ == '__main__':
    app.run(debug=True)
