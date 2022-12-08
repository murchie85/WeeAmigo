from flask import Flask, render_template, session, request, redirect
from tableFunctions import *
from gameFunctions import *
import sqlite3
import os
import json

#------ DEFINE APP

app = Flask(__name__)

#------ CREATE DB IF NOT EXIST
initDB()

#------ CLEAR SESSION ON FIRST LOAD
# create a variable to keep track of whether the session has been cleared
session_cleared = False

# create a function that will clear the session, but only once
@app.before_request
def clear_session():
    global session_cleared
    if not session_cleared:
        session.clear()
        session_cleared = True
        print("Clearing sessions")



#------ SECRET

# Use Flask's user session management system to store the user's credentials in a database
app.secret_key = 'SECRET_KEY'


#------ LANDING

@app.route('/')
def index():
  print('REDIRECTING TO LOGIN PAGE')
  # If the user is not logged in, render the login form
  return render_template('login.html')


#------ LOGIN

@app.route('/login', methods=['POST'])
def login():
  print("POSTING LOG IN ")

  # ATTEMPT TO CONNECT - CREATE TABLE IF NOT EXIST
  checkUserTableExists()

  # Read the username and password from the form
  username = request.form['username']
  password = request.form['password']

  user = returnUser(username, password)
  # If the username and password are correct, store the user's information in the session
  if user:
    print('****LOGGING IN USER *****')
    session['id']       = user[0]
    session['username'] = user[1]

    return redirect('/game')
  else:
    # If the username and password are incorrect, render the login form again with an error message
    return render_template('login.html', error='Incorrect username or password')






#------ SIGNUP

@app.route('/signup', methods=['GET', 'POST'])
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
    gameInstance      = Game(pet_name,username)

    print("*****Creating user")
    createUser(_id, username,pet_name,password,gameInstance)

    return redirect('/')
  


  if request.method == 'GET':
    return render_template('signup.html')


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






# route for the game page
@app.route('/game')
def game():
  if 'username' in session and 'id' in session:
    print('RENDERING MAIN PAGE')
    
    # If the user is logged in, render the template that displays the pet's name and age
    _id     = session['id']
    uname   = session['username']
    gameDict,result    = retrieve_game(_id)
    
    # IF GAME NOT LOADED 
    if(gameDict==None):
      return 'Something went wrong..contact the dev.'
    
    # IF FAILURE INSTANTIATING GAME
    try:
      gameInstance = Game(gameDict['pet'],gameDict['name'],gameDict['timer'],gameDict['age'])
    except:
      return 'Something went wrong..contact the dev.'


    gameInstance.run_game()

    return render_template('index.html', username=gameInstance.name, pet_name=gameInstance.pet, pet_age=gameInstance.age )
  else:
    return 'Something went wrong..contact the dev.'


@app.route('/clear')
def clear_session():
    session.clear()
    return 'Session cleared!'


#------ AUTO RUN

# run the app
if __name__ == '__main__':
  app.run()
