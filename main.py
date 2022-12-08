from flask import Flask, render_template, session, request, redirect


# ROUTES
from routes.index import index
from routes.login import login
from routes.signup import signup

# FUNCTIONS 
from tableFunctions import *
from gameFunctions import *
import sqlite3
import os
import json

#------ DEFINE APP

app = Flask(__name__)

# Register the index() function as the handler for the '/' route
app.route('/')(index)
app.route('/login', methods=['POST'])(login)
app.route('/signup', methods=['GET', 'POST'])(signup)



#------ CREATE DB IF NOT EXIST
initDB()

#------ CLEAR SESSION ON FIRST LOAD

session_cleared = False
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




import json

# game class with run_game function
class Game:
  def __init__(self, pet,name,timer=0,age=0):
    self.pet   = pet
    self.name  = name
    self.timer = timer
    self.age   = age

  def increment_timer(self):
    self.timer += 1
    self.age = self.timer / 3600

  def to_json(self):
    # Create a dictionary representing the Pet object
    self_dict = {
      "pet":   self.pet,
      "name":  self.name,
      "timer": self.timer,
      "age":   self.age
    }
    return(self_dict)

  def run_game(self):
    self.increment_timer()
    print('running')


#------ AUTO RUN

# run the app
if __name__ == '__main__':
  app.run()
