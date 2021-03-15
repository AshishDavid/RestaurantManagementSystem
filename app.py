from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('resto.html')


@app.route('/Menu')
def Menu():
    return render_template('menu.html')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
