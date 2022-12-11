#------ LANDING
from flask import Flask, render_template, session, request, redirect
from tableFunctions import *
from gameFunctions import *

#------ SIGNUP
def signup():
  if request.method == 'POST':

    # ATTEMPT TO CONNECT - CREATE TABLE IF NOT EXIST
    checkUserTableExists()

    # ------------CREATE USER 


    # Read the user's name, pet's name, and password from the form
    username = request.form['username']
    pet_name = request.form['pet_name']
    password = request.form['password']

    # connect to the database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # retrieve all data from the users table
    c.execute('SELECT * FROM users')
    rows = c.fetchall()

    # close the database connection
    conn.close()

    # ASSIGN UNIQUE ID
    validIDs = []
    # print the data
    for row in rows:
      validIDs.append(row[0])

    _id      = max(validIDs,default=0) + 1

    # INITIALISING GAME OBJECT
    # Create a Game instance with the Pet instance
    print("Creating game instance for " + str(username) + 'pet name is ' + str(pet_name))
    gameInstance      = Game(_id,pet_name,username)

    print("*****Creating user")
    createUser(_id, username,pet_name,password,gameInstance)

    return redirect('/')
  


  if request.method == 'GET':
    return render_template('signup.html')

