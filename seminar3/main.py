from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.security import generate_password_hash
from models import db, Users

import secrets

app = Flask(__name__)
app.secret_key = str(secrets.token_hex())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    new_user = Users(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/users')
def users():
    users = db.session.query(Users).all()
    if len(users) == 0:
        abort(404)
    return render_template('users.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)