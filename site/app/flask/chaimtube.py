from flask import *
import pymysql
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(128) # CSRF protection

check = 1
while check == 1:
    try:
        check = 0
        db = pymysql.connect('chaimtube_db', 'root', 'changeme', 'chaimtube')
    except pymysql.err.OperationalError:
        check = 1

cursor = db.cursor()

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username'] 
    password = request.form['password']
    
    cursor.execute("SELECT PasswordHash FROM Account WHERE Username='"+str(username)+"'")
    password_hash = cursor.fetchone()[0]
    if password_hash == password:
        session['Username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('incorrect.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/incorrect")
def incorrect():
    return render_template("incorrect.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('Username', None)
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')