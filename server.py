#!/usr/bin/python3

import os
import sys
import sqlite3 as sql
from bottle import route, run, post, request, template

if not os.path.exists('users.db'):
	users_db = sql.connect('users.db')
	users_cursor = users_db.cursor()
	users_cursor.execute("CREATE TABLE users_table(uname varchar(50), fname varchar(50), lname varchar(50), mob varchar(10), pwd varchar(30));")
	users_cursor.execute("CREATE TABLE items(uname varchar(50), item_name varchar(50), no_of_items int);")
	users_db.commit()
	users_db.close()

users_db = sql.connect('users.db')
users_cursor = users_db.cursor()

file_names = []

@route('/view')
def view_page():
    tpl_file = open('view.html')
    tpl = tpl_file.read()
    tpl_file.close()
    return template(tpl, table=[["NO Data","NO Data" ], ["NO Data","NO Data" ]])

@post('/add_user')
def add_user():
    uname = request.forms.get('uname')
    fname = request.forms.get('fname')
    lname = request.forms.get('lname')
    mob = request.forms.get('mob')
    pwd = request.forms.get('pwd')
    users_cursor.execute(f'INSERT INTO users_table VALUES ("{uname}", "{fname}", "{lname}", "{mob}", "{pwd}");')
    users_db.commit()
    return 'Signup Success!'

@post('/view')
def view():
    uname = request.forms.get('uname')
    pwd = request.forms.get('pwd')
    users_cursor.execute(f'SELECT pwd FROM users_table WHERE uname="{uname}";')
    correct_pwd = users_cursor.fetchall()[0][0]
    if pwd == correct_pwd:
        users_cursor.execute(f'SELECT * FROM items WHERE uname="{uname}";')
        tpl_file = open('view.html')
        tpl = tpl_file.read()
        tpl_file.close()
        return template(tpl, table=users_cursor.fetchall())
    else:
        return 'Incorrect Password <a href="/">Click here to go back</a>'

@route('/')
def default_page():
    if not file_names:
        for f in os.listdir('.'):
            file_names.append(os.path.splitext(f)[0][0])
    page_file = open('index.html')
    page = page_file.read()
    page_file.close()
    return page

@route('/<page>')
def hello(page=''):
    if not file_names:
        for f in os.listdir('.'):
            file_names.append(os.path.splitext(f)[0])
    if page in file_names: 
        page_file = open(page + '.html')
        page = page_file.read()
        page_file.close()
        return page
    else:
        return 'This page does not exist yet, <a href="/">Click here to go back</a>'

run(host='localhost', port=8080, debug=True)
