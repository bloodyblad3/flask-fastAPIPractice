import secrets
from flask import Flask, render_template, request, make_response, session, redirect, url_for

app = Flask(__name__)
app.secret_key = str(secrets.token_hex())

@app.route("/")
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], email=session['user_email'])
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username', None)
        session['user_email'] = request.form.get('email', None)
        
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)