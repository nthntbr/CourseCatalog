import datetime
import os
import re
import pandas as pd
from flask import Flask, redirect, render_template, session, request
from flask_socketio import SocketIO, emit
from src.Class_Search_Method import Local_Course_Catalogue
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'secret_key'
socketio = SocketIO(app)
# socket allows the use of javascript to communicate data with html pages

course_catalogue = Local_Course_Catalogue("csuCourseCatalogDB")
#reference to coures catalog DB

session_cache = {}

def cache_session_data(session_id, data):
    """Cache session data using a unique session identifier."""
    session_cache[session_id] = data

def get_cached_session_data(session_id):
    """Retrieve cached session data using a unique session identifier."""
    return session_cache.get(session_id, None)

def clear_session_data(session_id):
    """Clear session data for a given session identifier."""
    if session_id in session_cache:
        del session_cache[session_id]


def ack():
    print('message was received!')



# Code for home page
@app.route('/')
def home():
    
    return render_template('/index.html')

# Code for search page
@app.route("/search")
def search():

    return render_template('/search.html')

# Code for department page
@app.route('/department')
def department():
    session_id = request.args.get('session_id')
    if not session_id:
        return 'Session ID not provided', 400

    department_code = get_cached_session_data(session_id)
    if not department_code:
        return 'Invalid or expired session', 400
    
    names = get_cached_session_data('departmentNames')
    cache_session_data('departmentCode', department_code)
    department = "ERROR!"
    for name in names:
        if name[1] == department_code:
            department = name[0]
            break
    


    #may want to delete not sure
    #clear_session_data(session_id)
    return render_template('department.html', department=department)

# Code for course page
@app.route("/course")
def course():
    session_id = request.args.get('session_id')
    if not session_id:
        return 'Session ID not provided', 400

    course_code = get_cached_session_data(session_id)
    
    if not course_code:
        return 'Invalid or expired session', 400
    parts = course_code.split("\xa0")

    if len(parts) == 2:
        part1 = parts[0].strip()
        part2 = parts[1].strip()
        print("Part 1: " + part1)
        print("Part 2: " + part2)
    else:
        print("Invalid input string format.")
    clear_session_data('departmentCode')
    cache_session_data('departmentCode', parts[0])
    department = "ERROR!"
    names = get_cached_session_data('departmentNames')
    for name in names:
        if name[1] == parts[0]:
            department = name[0]
            break
    
    clear_session_data('courseCode')
    cache_session_data('courseCode', course_code)
    
    
    return render_template('/course.html', department=department)







@socketio.on('isConnected')
def isConnected(data):
    print(data)
    if data['data'] == 'index':        
        departments = loadDepartments()
        session['departments'] = departments
        socketio.emit('departmentsUpdate', session['departments'])
    elif data['data'] == 'department':
        if 'departments' not in session:
            departments = loadDepartments()
            session['departments'] = departments
            socketio.emit('departmentsUpdate', session['departments'])
        #print(session['selected_department'])
    if data['data'] == 'department':
        print("Connected to department!")
        print("Loading Courses...\n")
        loadCourseList()
    if data['data'] == 'course':
        print("Connected to course!")
        print("Loading Course...\n")
        loadCourse()

def loadCourseList():
    department_code = get_cached_session_data('departmentCode')  # Retrieve the department code from the data parameter
    df = course_catalogue.search_course_catalogue_by_terms(-1, department_code, "", "", "", "", "", "")
    json = df.to_json(orient='records')
    socketio.emit('courseListUpdate', json, callback=ack)

def loadCourse():
    department_code = get_cached_session_data('departmentCode')  # Retrieve the department code from the data parameter
    course_code = get_cached_session_data('courseCode')
    print("Department Code: " + department_code)

    print("Course Code: " + course_code)
    df = course_catalogue.search_course_catalogue_by_terms(-1, course_code, "", "", "", "", "", "")
    json = df.to_json(orient='records')
    print(json)
    socketio.emit('courseListUpdate', json, callback=ack)



@socketio.on('departmentButtonClicked')
def handle_department_click(data):
    session_id = str(uuid4())
    cache_session_data(session_id, data['code'])
    print("test")
    emit('redirect_to_department', {'session_id': session_id}, to=request.sid)


@socketio.on('courseClicked')
def handle_course_click(data):
    session_id = str(uuid4())
    cache_session_data(session_id, data['code'])
    emit('redirect_to_course', {'session_id': session_id}, to=request.sid)


def loadDepartments():
    df = course_catalogue.search_course_catalogue_by_terms(-1, "", "", "", "", "", "", "")
    return loadAtoZ(df)

def loadAtoZ(data):
    path = 'csuCourseCatalogDB'
    contents = os.listdir(path)
    departments = []
    pattern = r'\((.*?)\)'
    for department in contents:
        s = department.replace('_', ' ')
        match = re.search(pattern, s)

        if match:
            # Get the matched text (department code)
            code = match.group(1)
            # Split the input string into department name and the rest
            department_name, _ = s.split(f' ({code})')
            # Append the department name and code as a tuple to the list
            departments.append((department_name, code))
    #Alphabetical Order
    departments = sorted(departments, key=lambda x: x[0])
    #print(departments)
    cache_session_data('departmentNames', departments)
    return departments


