from flask import Flask, flash, redirect, render_template, request, session, abort
import pymysql

app = Flask(__name__)

check = 1
while check == 1:
    try:
        check = 0
        db = pymysql.connect('chaimtube_db', 'root', 'changeme', 'chaimtube')
    except pymysql.err.OperationalError:
        #print("Database not yet ready. Retrying...")
        check = 1

cursor = db.cursor()

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username'] 
    password = request.form['password']
    
    cursor.execute("SELECT user_id FROM Account WHERE Username="+"'"+str(username)+"'")
    id = cursor.fetchone()
    return "Logging in user " + id + "."

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/wrongpass")
def wrongpass():
    return render_template("wrongpass.html")

@app.route("/wronguser")
def wronguser():
    return render_template("wronguser.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')