import MySQLdb.cursors
from os.path import join, dirname, realpath
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
app.config['UPLOAD_FOLDER'] = '/static/Images'
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/Images')


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
                session['accountType'] = account['accountType']
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


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'GET':
        return render_template('Orders/cart.html')


@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'GET':
        return render_template('Management/index.html')


@app.route('/managecategories', methods=['GET', 'POST'])
def managecategories():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM categories WHERE enabled = 1')
        categoriesresult = cursor.fetchall()
        cursor.close()
        return render_template('Management/categories.html', data=categoriesresult)


@app.route('/managedishes', methods=['GET', 'POST'])
def managedishes():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT itd.*,ct.name AS categoryname FROM itemdishes itd JOIN categories ct ON itd.categoryId = ct.id WHERE itd.enabled = 1')
        dishesresult = cursor.fetchall()
        cursor.close()
        return render_template('Management/dishes.html', data=dishesresult)


@app.route('/createcategory', methods=['GET', 'POST'])
def createcategory():
    if request.method == 'GET':
        return render_template('Categories/create.html')
    else:
        namecat = request.form['namecategory']
        file1 = request.files['imageCategory']
        path = join(UPLOADS_PATH, file1.filename)
        file1.save(path)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO categories (name, imagePath, enabled) VALUES (%s, %s, %s)",
                       (namecat, join("static/images", file1.filename), True))
        mysql.connection.commit()

        return redirect(url_for("manage"))


@app.route('/deletecategory', methods=['GET', 'POST'])
def deletecategory():
    if request.method == 'GET':
        idcategory = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE categories SET enabled = 0 WHERE id = %s", idcategory)
        mysql.connection.commit()
        cursor.close()

    return redirect(url_for("managecategories"))


@app.route('/editcategory', methods=['GET', 'POST'])
def editcategory():
    if request.method == 'GET':
        idcategory = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM categories WHERE id = %s', idcategory)
        categoriesresult = cursor.fetchall()
        cursor.close()
        return render_template('Categories/edit.html', data=categoriesresult)

    else:
        idcat = request.form['idcategory']
        namecat = request.form['namecategory']
        imagepath = ''
        if request.files['imageCategory'].filename != '':
            file1 = request.files['imageCategory']
            path = join(UPLOADS_PATH, file1.filename)
            file1.save(path)
            imagepath = file1.filename
        else:
            imagepath = request.form['imagepath']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE categories SET name = %s, imagePath = %s WHERE id = %s", (namecat, imagepath, idcat))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("managecategories"))


@app.route('/createdishes', methods=['GET', 'POST'])
def createdishes():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM categories WHERE enabled = 1')
        categoriesresult = cursor.fetchall()
        cursor.close()
        return render_template('Dishes/create.html', data=categoriesresult)
    else:
        namedish = request.form['namedish']
        pricedishes = request.form['pricedishes']
        descriptiondishes = request.form['descriptiondishes']
        categoryselect = str(request.form.get('categorySelect'))
        filedish = request.files['imagedishes']
        pathdishes = join(UPLOADS_PATH, filedish.filename)
        filedish.save(pathdishes)

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO itemdishes (name, description, price, categoryId, imagePath, enabled) VALUES (%s, %s, %s, %s, %s, %s)",
            (namedish, descriptiondishes, pricedishes, categoryselect, join("static/images", filedish.filename), True))
        mysql.connection.commit()

        return redirect(url_for("managedishes"))


@app.route('/deletedishes', methods=['GET', 'POST'])
def deletedishes():
    if request.method == 'GET':
        iditemdishes = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE itemdishes SET enabled = 0 WHERE id = %s", iditemdishes)
        mysql.connection.commit()
        cursor.close()

    return redirect(url_for("managedishes"))


@app.route('/editdishes', methods=['GET', 'POST'])
def editdishes():
    if request.method == 'GET':
        idcategory = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM itemdishes WHERE id = %s', idcategory)
        dishresult = cursor.fetchall()
        cursor.close()
        return render_template('Dishes/edit.html', data=dishresult)

    else:
        id = request.form['iddishes']
        namedish = request.form['namedish']
        pricedishes = request.form['pricedishes']
        descriptiondishes = request.form['descriptiondishes']
        imagepath = ''
        if request.files['imagedishes'].filename != '':
            file1 = request.files['imagedishes']
            path = join(UPLOADS_PATH, file1.filename)
            file1.save(path)
            imagepath = file1.filename
        else:
            imagepath = request.form['imagepath']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE itemdishes SET name = %s, description = %s, price = %s, imagePath = %s WHERE id = %s", (namedish, descriptiondishes, pricedishes, imagepath, id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("managedishes"))


if __name__ == '__main__':
    app.run(debug=True)
