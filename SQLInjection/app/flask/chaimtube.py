from flask import *
import hashlib
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
    
    #sql_statement = "SELECT Salt from Account WHERE Username=%s"    # SQL Injection (classic) protection
    #ursor.execute(sql_statement, str(username))

    cursor.execute("SELECT Salt from Account WHERE Username="+"'"+str(username)+"'")
    salt = cursor.fetchone()

    if salt is None:
        return render_template('incorrectuser.html')
    else:
        salt = salt[0]



    calculated_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    #sql_statement = "SELECT PasswordHash FROM Account WHERE Username=%s"
    #cursor.execute(sql_statement, str(username))
    cursor.execute("SELECT PasswordHash FROM Account WHERE Username="+"'"+str(username)+"'")
    password_hash = cursor.fetchone()[0]
    
    if password_hash == calculated_hash:
        #sql_statement = "SELECT DisplayName from Account WHERE Username=%s"
        #cursor.execute(sql_statement, str(username))
        cursor.execute("SELECT DisplayName from Account WHERE Username="+"'"+str(username)+"'")
        display_name = cursor.fetchone()[0]

        session['Username'] = display_name
        return redirect(url_for('home'))
    else:
        cursor.execute("SELECT * FROM Account WHERE Username="+"'"+str(username)+"'")
        all = cursor.fetchall()
        return render_template('incorrectpassword.html', error=all)

@app.route("/home")
def home():
    return render_template("home.html", username = session['Username'])

#@app.route("/incorrect")
#def incorrect():
#    return render_template("incorrect.html")

@app.route("/incorrectuser")
def incorrectuser():
    return render_template("incorrectuser.html")


@app.route("/incorrectpassword")
def incorrectpassword():
    return render_template("incorrectpassword.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('Username', None)
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
