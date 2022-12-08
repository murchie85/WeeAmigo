#------ LANDING
from flask import Flask, render_template, session, request, redirect
from tableFunctions import *
from gameFunctions import *


# create a route that will handle the request
@app.route('/users')
def get_users():
    # connect to the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # retrieve all data from the users table
    c.execute('SELECT * FROM users')
    rows = c.fetchall()

    # close the database connection
    conn.close()

    # print the data
    for row in rows:
        print(row)

    return 'Data retrieved successfully'



