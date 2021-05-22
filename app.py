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

app.secret_key = 'monica'


@app.route('/')
def home():
    return render_template('resto.html')


@app.route('/welcome')
def welcome():
    return render_template('Home/index.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        return render_template('Feedback/index.html')
    else:
        descriptiontext = request.form['feedbackDescription']
        userlogged = request.form['userlogged']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO feedback (description) VALUES (%s)", [descriptiontext])
        mysql.connection.commit()

        if userlogged == 'True':
            return redirect(url_for("welcome"))
        else:
            return render_template('resto.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('Shared/Contact.html')
    else:
        name = request.form['nameContact']
        email = request.form['emailcontact']
        descriptiontext = request.form['messageDescription']
        userlogged = request.form['userlogged']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO contact (name, email, description) VALUES (%s, %s, %s)",
                       (name, email, descriptiontext))
        mysql.connection.commit()

        if userlogged == 'True':
            return redirect(url_for("welcome"))
        else:
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

        return redirect(url_for("welcome"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'usernameOrEmail' in request.form and 'password' in request.form:
        username_or_email = request.form['usernameOrEmail']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s OR email = % s',
                       (username_or_email, username_or_email))
        account = cursor.fetchone()
        if account:
            if bcrypt.hashpw(password, account['password'].encode('utf-8')) == account['password'].encode('utf-8'):
                session['name'] = username_or_email
                return redirect(url_for("welcome"))
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


@app.route('/team')
def team():
    return render_template('Shared/Team.html')


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM categories WHERE enabled = 1')
        categoriesresult = cursor.fetchall()
        cursor.close()

    return render_template('Categories/index.html', data=categoriesresult)


@app.route('/itemsdishes', methods=['GET', 'POST'])
def itemsdishes():
    if request.method == 'GET':
        idcategory = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM itemdishes WHERE enabled = 1 and categoryId = % s', idcategory)
        dishesresult = cursor.fetchall()
        cursor.close()

    return render_template('Dishes/index.html', data=dishesresult)


if __name__ == '__main__':
    app.run(debug=True)
