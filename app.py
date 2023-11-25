import datetime
import os
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from src.Class_Search_Method import Local_Course_Catalogue


app = Flask(__name__)
app.secret_key = 'secret_key'
socketio = SocketIO(app)
# socket allows the use of javascript to communicate data with html pages

course_catalogue = Local_Course_Catalogue("csuCourseCatalogDB")
#reference to coures catalog DB


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


@socketio.on('isConnected')
def isConnected(data):
    print("Test")
    data = course_catalogue.search_course_catalogue_by_terms(-1, "", "", "", "", "", "", "")
    print("DB: Data: " + str(data))
