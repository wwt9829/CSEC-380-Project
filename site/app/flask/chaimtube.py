import filetype
from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
import pymysql
import os
import requests
import sys                                                                              # remove

# MAIN

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(128)                                              # CSRF protection
session_id = None

limiter = Limiter(                                                                      # Brute force protection
    app,
    key_func=get_remote_address
)

def db_connect():    
    check = 1
    while check == 1:
        try:
            check = 0
            db = pymysql.connect(host='chaimtube_db', user='root', passwd='changeme', db='chaimtube', autocommit=True)
        except pymysql.err.OperationalError:
            check = 1

    cursor = db.cursor()
    return cursor, db

@app.route("/", methods=["GET"])
def landing():
    return render_template("login.html")

# LOGIN

@app.route("/login", methods=["POST"])
@limiter.limit("10 per minute", error_message="You have tried to log in too many times. Please wait a moment and try again.")        # Brute force protection
def login():
    global session_id

    cursor, db = db_connect()
    
    username = request.form['username'] 
    password = request.form['password']
    
    sql_statement = "SELECT Salt from Account WHERE Username=%s;"                       # SQL Injection (classic) protection
    cursor.execute(sql_statement, str(username))
    salt = cursor.fetchone()

    if salt is None:
        cursor.close()
        db.close()
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

        session['logged_in'] = True
        session_id = os.urandom(128)  
        session['session_id'] = session_id

        cursor.close()
        db.close()
        return redirect(url_for('home'))
    else:
        cursor.close()
        db.close()
        return render_template('incorrect.html')

@app.route("/incorrect", methods=["GET"])
def incorrect():
    return render_template("incorrect.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('session_id', None)
    session.pop('user_id', None)
    session.pop('display_name', None)
    session.pop('logged_in', None)
    
    return redirect(url_for('landing'))

# HOMEPAGE

@app.route("/home", methods=["GET", "POST"])
def home():
    if session.get('logged_in') is None:
        return redirect(url_for('landing'))
    elif session.get('session_id') != session_id:
        return redirect(url_for('logout'))
    
    cursor, db = db_connect()

    # Upload by link
    link = request.form.get('linkupload', None)

    if link != "" and link is not None:
        try:
            video = requests.get(link.strip(), stream=True).content

            kind = filetype.guess(video)

            if kind is None or kind.extension != "mp4":
                cursor.close()
                db.close()
                return "Valid .mp4 file not found at " + link

            kind = kind.extension
            
            # Video metadata
            user_id = session['user_id']
            username = session['display_name']
            video_name = link.split('/')[-1]
            location = "video/" + video_name

            # Store video at location
            with open(location, 'wb') as code:
                code.write(video)
            
            # Store metadata in database
            sql_statement = "INSERT INTO Video(user_id, Username, FileName) VALUES (%s, %s, %s);"      # SQL Injection protection
            insert = (str(user_id), str(username), str(video_name))
            cursor.execute(sql_statement, insert)

        except requests.exceptions.MissingSchema:
            cursor.close()
            db.close()
            return "Invalid URL"
        
        cursor.close()
        db.close()
        return render_template("home.html", username = session['display_name'])

    # Upload by file
    elif request.files.getlist("file") is not None:
        for video in request.files.getlist("file"):
            
            # Video metadata
            user_id = session['user_id']
            username = session['display_name']
            video_name = video.filename

            # Store video at location
            try:
                video.save("video/" + video_name)
            except IsADirectoryError:
                return "Please submit a video to upload."

            # Store metadata in database
            sql_statement = "INSERT INTO Video(user_id, Username, FileName) VALUES (%s, %s, %s);"      # SQL Injection protection
            insert = (str(user_id), str(username), str(video_name))
            cursor.execute(sql_statement, insert)

        cursor.close()
        db.close()
        return render_template("home.html", username = session['display_name'])

    else:
        cursor.close()
        db.close()
        return render_template("home.html", username = session['display_name'])

@app.route("/getvideos", methods=["POST"])
def own_videos():
    if session.get('logged_in') is None:
        return redirect(url_for('landing'))
    elif session.get('session_id') != session_id:
        return redirect(url_for('logout'))

    cursor, db = db_connect()
    
    user_id = session['user_id']

    sql_statement = "SELECT * FROM Video WHERE user_id=%s;"                             # SQL Injection protection
    cursor.execute(sql_statement, str(user_id))
    own_video_info = cursor.fetchall()

    table_data=[x[0] for x in cursor.description]
    json_data=[]
    for data in own_video_info:
        json_data.append(dict(zip(table_data,data)))
    
    cursor.close()
    db.close()
    return jsonify(json_data)

@app.route("/getothervids", methods=["POST"])
def other_videos():
    if session.get('logged_in') is None:
        return redirect(url_for('landing'))
    elif session.get('session_id') != session_id:
        return redirect(url_for('logout'))

    cursor, db = db_connect()
    
    user_id = session['user_id']

    sql_statement = "SELECT * FROM Video WHERE user_id!=%s;"                             # SQL Injection protection
    cursor.execute(sql_statement, str(user_id))
    other_video_info = cursor.fetchall()

    table_data=[x[0] for x in cursor.description]
    json_data=[]
    for data in other_video_info:
        json_data.append(dict(zip(table_data,data)))
    
    cursor.close()
    db.close()
    return jsonify(json_data)

@app.route("/delete/<video_id>", methods=["GET"])
def delete_video(video_id):
    if session.get('logged_in') is None:
        return redirect(url_for('landing'))
    elif session.get('session_id') != session_id:
        return redirect(url_for('logout'))

    cursor, db = db_connect()

    sql_statement = "SELECT user_id FROM Video WHERE video_id=%s;"                       # SQL Injection protection
    cursor.execute(sql_statement, str(video_id))
    video_owner = cursor.fetchone()[0]

    user_id = session['user_id']

    if user_id == video_owner:
        sql_statement = "SELECT FileName FROM Video WHERE video_id=%s;"                  # SQL Injection protection
        cursor.execute(sql_statement, str(video_id))
        video_name = cursor.fetchone()[0]

        try:
            os.remove("video/" + video_name)
        except Exception as e:
            print(e, file=sys.stderr)

        sql_statement = "DELETE FROM Video WHERE video_id=%s;"                           # SQL Injection protection
        cursor.execute(sql_statement, str(video_id))
    else:
        return "Error: Video owned by different user. Cannot be deleted."

    cursor.close()
    db.close()
    return redirect(url_for('home'))

@app.route('/video/<title>', methods=["GET"])
def get_video(title):
    if session.get('logged_in') is None:
        return redirect(url_for('landing'))
    elif session.get('session_id') != session_id:
        return redirect(url_for('logout'))

    return send_from_directory('/video', title)

if __name__ == "__main__":
    app.run(host='0.0.0.0')