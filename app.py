import datetime
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'secret_key'
socketio = SocketIO(app)
# socket allows the use of javascript to communicate data with html pages

# Code for home page
@app.route('/')
def home():

    return render_template('/index.html')

# Code for search page
@app.route("/search")
def search():

    return render_template('/search.html')

# Code for department page
@app.route("/department")
def department():

    return render_template('/department.html')

# Code for course page
@app.route("/course")
def course():

    return render_template('/course.html')