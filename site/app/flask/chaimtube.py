import filetype
from flask import *
import hashlib
import pymysql
import os
import requests
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(128) # CSRF protection

print("Waiting for database connection...", file=sys.stderr)     
check = 1
while check == 1:
    try:
        check = 0
        db = pymysql.connect(host='chaimtube_db', user='root', passwd='changeme', db='chaimtube', autocommit=True)
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
    
    sql_statement = "SELECT Salt from Account WHERE Username=%s;"    # SQL Injection (classic) protection
    cursor.execute(sql_statement, str(username))
    salt = cursor.fetchone()

    if salt is None:
        return render_template('incorrect.html')
    else:
        salt = salt[0]

    calculated_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    sql_statement = "SELECT PasswordHash FROM Account WHERE Username=%s;"
    cursor.execute(sql_statement, str(username))
    password_hash = cursor.fetchone()[0]
    
    if password_hash == calculated_hash:
        sql_statement = "SELECT user_id from Account WHERE Username=%s;"
        cursor.execute(sql_statement, str(username))
        session['user_id'] = cursor.fetchone()[0]

        sql_statement = "SELECT DisplayName FROM Account WHERE Username=%s;"
        cursor.execute(sql_statement, str(username))
        session['display_name'] = cursor.fetchone()[0]

        return redirect(url_for('home'))
    else:
        return render_template('incorrect.html')

@app.route("/home", methods=["GET", "POST"])
def home():
    # Upload by link
    link = request.form.get('linkupload', None)

    if link != "" and link is not None:
        try:
            video = requests.get(link.strip(), stream=True).content

            kind = filetype.guess(video)

            if kind is None or kind.extension != "mp4":
                return "Valid .mp4 file not found at " + link

            kind = kind.extension
            
            # Video metadata
            user_id = session['user_id']
            video_name = link.split('/')[-1]
            location = "video/" + video_name

            # Store video at location
            with open(location, 'wb') as code:
                code.write(video)
            
            # Store metadata in database
            sql_statement = "INSERT INTO Video(user_id, FileName, VideoLocation) VALUES (%s, %s, %s);"      # SQL Injection protection
            insert = (str(user_id), str(video_name), str(location))
            cursor.execute(sql_statement, insert)

        except requests.exceptions.MissingSchema:
            return "Invalid URL"
        
        return render_template("home.html", username = session['display_name'])

    # Upload by file
    elif request.files.getlist("file") is not None:
        for video in request.files.getlist("file"):
            
            # Video metadata
            user_id = session['user_id']
            video_name = video.filename
            location = "video/" + video_name

            # Store video at location
            video.save("video/" + video_name)

            # Store metadata in database
            sql_statement = "INSERT INTO Video(user_id, FileName, VideoLocation) VALUES (%s, %s, %s);"      # SQL Injection protection
            insert = (str(user_id), str(video_name), str(location))
            cursor.execute(sql_statement, insert)

        return render_template("home.html", username = session['display_name'])

    else:
        return render_template("home.html", username = session['display_name'])

@app.route("/incorrect")
def incorrect():
    return render_template("incorrect.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('Username', None)
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')