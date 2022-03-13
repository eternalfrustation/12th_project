users_db = mysql.connector.connect(
    host=input("Enter the host name"),
    user=input("Enter the username for the sql server"),
    port=input("Enter the port, the sql server is running on"),
    password=input("Enter the password for the sql server"),
)
users_cursor = users_db.cursor()
users_cursor.execute("CREATE DATABASE users;")
users_cursor.execute("CREATE TABLE users_table(fname varchar(20), lname varchar(20), mob varchar(10), pwd varchar(30), uname varchar(50));")
users_cursor.execute("CREATE TABLE items(uname varchar(50), item_name varchar(50), no_of_items int);")