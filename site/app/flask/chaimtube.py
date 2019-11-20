import filetype
from flask import *
import hashlib
import pymysql
import os
import requests
import sys          # disable if only used for printing

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
    
    sql_statement = "SELECT Salt from Account WHERE Username=%s"    # SQL Injection (classic) protection
    cursor.execute(sql_statement, str(username))
    salt = cursor.fetchone()

    if salt is None:
        return render_template('incorrect.html')
    else:
        salt = salt[0]

    calculated_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    sql_statement = "SELECT PasswordHash FROM Account WHERE Username=%s"
    cursor.execute(sql_statement, str(username))
    password_hash = cursor.fetchone()[0]
    
    if password_hash == calculated_hash:
        sql_statement = "SELECT DisplayName from Account WHERE Username=%s"
        cursor.execute(sql_statement, str(username))
        display_name = cursor.fetchone()[0]

        session['Username'] = display_name
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
            kind = filetype.guess(video).extension

            if kind != "mp4":
                return "Valid .mp4 file not found at " + link
            
            # Video metadata
            sql_statement = "SELECT user_id FROM Account WHERE Username=%s"
            user = session['Username']
            cursor.execute(sql_statement, user)
            user_id = cursor.fetchone()[0]

            video_name = link.split('/')[-1]
            location = "video/" + name

            # Store video at location
            with open(location) as code:
                code.write(video, "wb")
            
            # Store metadata in database
            cursor.execute("INSERT INTO Video(user_id, FileName, VideoLocation) VALUES ('{}', '{}', '{}')".format(user_id, video_name, location))

        except requests.exceptions.MissingSchema:
            return "Invalid URL"
        except TypeError:
            return "Valid .mp4 file not found at " + link
        
        return render_template("home.html", username = session['Username'])

    # Upload by file
    elif request.files.getlist("file") is not None:
        for video in request.files.getlist("file"):
            
            # Video metadata
            sql_statement = "SELECT user_id FROM Account WHERE Username=%s"
            user = session['Username']
            cursor.execute(sql_statement, user)
            user_id = cursor.fetchone()[0]

            video_name = video.filename
            location = "video/" + video_name

            # Store video at location
            video.save("video/" + video_name)

            # Store metadata in database
            cursor.execute("INSERT INTO Video(user_id, FileName, VideoLocation) VALUES ('{}', '{}', '{}')".format(user_id, video_name, location))

        return render_template("home.html", username = session['Username'])

    else:
        print("Someone did nothing", file=sys.stderr)                           # remove
        return render_template("home.html", username = session['Username'])

@app.route("/incorrect")
def incorrect():
    return render_template("incorrect.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('Username', None)
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')