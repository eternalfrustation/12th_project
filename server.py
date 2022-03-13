from bottle import route, run, post, request, template
import mysql.connector
import os
file_names = []

users_db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port="3306",
    password="sql123",
    database="users"
)
users_cursor = users_db.cursor()

@route('/view')
def view_page():
    tpl_file = open("view.html")
    tpl = tpl_file.read()
    tpl_file.close()
    return template(tpl, table=[["NO Data","NO Data" ], ["NO Data","NO Data" ]])

@post('/add_user')
def add_user():
    uname = request.forms.get("uname")
    fname = request.forms.get("fname")
    lname = request.forms.get("lname")
    mob = request.forms.get("mob")
    pwd = request.forms.get("pwd")
    users_cursor.execute("INSERT INTO users_table (uname, fname, lname, mob, pwd) VALUES (%s, %s, %s, %s, %s);", (uname, fname, lname, mob, pwd))
    users_db.commit()

@post('/view')
def view():
    uname = request.forms.get("uname")
    pwd = request.forms.get("pwd")
    users_cursor.execute("SELECT pwd FROM users_table WHERE uname=\"%s\";" % (uname))
    correct_pwd = users_cursor.fetchall()[0][0]
    if pwd == correct_pwd:
        users_cursor.execute("SELECT * FROM items WHERE uname=\"%s\";" % (uname))
        tpl_file = open("view.html")
        tpl = tpl_file.read()
        tpl_file.close()
        return template(tpl, table=users_cursor.fetchall())
    else:
        return "Incorrect Password <a href=\"/\">Click here to go back</a>"

@route('/')
def default_page():
    if not file_names:
        for f in os.listdir('.'):
            file_names.append(os.path.splitext(f)[0][0])
    page_file = open("index.html")
    page = page_file.read()
    page_file.close()
    return page

@route('/<page>')
def hello(page=""):
    if not file_names:
        for f in os.listdir('.'):
            file_names.append(os.path.splitext(f)[0])
    if page in file_names: 
        page_file = open(page + ".html")
        page = page_file.read()
        page_file.close()
        return page
    else:
        return "This page does not exist yet, <a href=\"/\">Click here to go back</a>"

run(host='localhost', port=8080, debug=True)