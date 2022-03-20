#!/usr/bin/python3

import os
import sys
import sqlite3 as sql
from bottle import route, run, post, request, template, static_file, get
import json




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

@post('/view_json')
def view_json():
    uname = request.forms.get('uname')
    pwd = request.forms.get('pwd')
    users_cursor.execute(f'SELECT pwd FROM users_table WHERE uname="{uname}";')
    correct_pwd = users_cursor.fetchall()[0][0]
    if pwd == correct_pwd:
        users_cursor.execute(f'SELECT * FROM items WHERE uname="{uname}";')
        return json.dumps(users_cursor.fetchall())
    else:
        return '{status: "Error"}'

@route('/view')
def view_page():
    tpl_file = open('view.html')
    tpl = tpl_file.read()
    tpl_file.close()
    return template(tpl, table=[["NO Data","NO Data" ], ["NO Data","NO Data" ]])

@route('/signup')
def view_page():
    tpl_file = open('signup.html')
    tpl = tpl_file.read()
    tpl_file.close()
    return template(tpl, table=[["NO Data","NO Data" ], ["NO Data","NO Data" ]])

@route('/modify')
def view_page():
    tpl_file = open('modify.html')
    tpl = tpl_file.read()
    tpl_file.close()
    return template(tpl, table=[["NO Data","NO Data" ], ["NO Data","NO Data" ]])

@post('/modify')
def mod_table():
    uname = request.forms.get('uname')
    pwd = request.forms.get('pwd')
    command = request.forms.get('command')
    item_name = request.forms.get('item_name')
    item_no = request.forms.get('item_no')
    users_cursor.execute(f'SELECT pwd FROM users_table WHERE uname="{uname}";')
    correct_pwd = users_cursor.fetchall()[0][0]
    if pwd == correct_pwd:
        if command == "Add":
            users_cursor.execute(f'SELECT no_of_items FROM items WHERE uname="{uname}" AND item_name="{item_name}";')
            item_quantities = users_cursor.fetchall()
            if len(item_quantities) == 0:
                print(f'INSERT INTO items VALUES ("{uname}", "{item_name}", {item_no});')
                users_cursor.execute(f'INSERT INTO items VALUES ("{uname}", "{item_name}", {item_no});')
            if len(item_quantities) == 1:
                new_item_quantity = int(item_quantities[0][0]) + int(item_no)
                users_cursor.execute(f'UPDATE items SET no_of_items={new_item_quantity} WHERE uname="{uname}" AND item_name="{item_name}";')
            if len(item_quantities) > 1:
                new_item_quantity = int(item_no)
                for item_quantity_string in item_quantities:
                    prexisting_item_quantity += int(item_quantity_string)
                    users_cursor.execute(f'UPDATE items SET no_of_items={new_item_quantity} WHERE uname="{uname}" AND item_name="{item_name}";')
        elif command == "Del":
            users_cursor.execute(f'DELETE FROM items WHERE item_name="{item_name}"')
        elif command == "Mod":
            users_cursor.execute(f'UPDATE items SET no_of_items={item_no} WHERE item_name="{item_name}"')
        users_db.commit()
        return '{status: "Success"}'
    else:
        return '{status: "Incorrect Password"}'

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
       
       
       
       
@get('/static/:filename#.*#')
def serve_static(filename):
	return static_file(filename, root='static')
    
    
    
    
@route('/')
def default_page():
    if not file_names:
        for f in os.listdir('.'):
            file_names.append(os.path.splitext(f)[0][0])
    page_file = open('index.html')
    page = page_file.read()
    page_file.close()
    return page

run(host='localhost', port=8080, debug=True)
