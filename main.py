#os.environ['FLASK_SOCKETIO_SERVER_ADDRESS'] = 'http://127.0.0.1:5000'
#socketio = SocketIO(app, server_address='http://127.0.0.1:5000/')

from flask import Flask, render_template, session, request, redirect
import time 
# THREADING
from flask_socketio import SocketIO, emit
from threading import Thread

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
#socketio = SocketIO(app)



# Register the index() function as the handler for the '/' route
app.route('/',methods=['GET'])(index)
app.route('/login', methods=['GET', 'POST'])(login)
app.route('/signup', methods=['GET', 'POST'])(signup)

# This makes it compatible with sockets
#app.add_url_rule('/', 'index', index)
#app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
#app.add_url_rule('/signup', 'signup', signup, methods=['GET', 'POST'])




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




# ----------SOCKET 



# Route for the game page
@app.route('/game')
def game():
  if 'username' in session and 'id' in session:
    print('RENDERING MAIN PAGE FROM GAME PAGE')
    
    # If the user is logged in, render the template that displays the pet's name and age
    _id     = session['id']
    uname   = session['username']
    gameDict,result    = retrieve_game(_id)
    
    # IF GAME NOT LOADED 
    if(gameDict==None):
      return 'Something went wrong..contact the dev.'
    
    # IF FAILURE INSTANTIATING GAME
    try:
      gameInstance = Game(_id,gameDict['pet'],gameDict['name'],gameDict['timer'],gameDict['age'])
    except:
      return 'Something went wrong..contact the dev.'
    
    # Start a timer to update the game state at regular intervals
    if(session['threadStarted']==False):
      print('STARTING BACKGROUND SOCKET TASK')
      # Create a new thread to run the update_game_state() function
      update_game_thread = Thread(target=update_game_state, args=(gameInstance,))
      # Start the thread
      update_game_thread.start()
      session['threadStarted'] = True


    return render_template('index.html', username=gameInstance.name, pet_name=gameInstance.pet, pet_age=gameInstance.age,time_elapsed=gameInstance.timer )
  else:
    return 'Something went wrong..contact the dev.'



# Function that updates the game state and sends updates to the client
def update_game_state(game_instance):
  while True:
    
    print('running: ', str(game_instance.timer), str(game_instance.age))
    game_instance.run_game()

    # UPDATE DB with latest value
    store_game(game_instance, game_instance._id)


    # Wait a short time before sending the next update
    time.sleep(1)


@app.route('/update_data')
def update_data():
  try:
    _id                = session['id']
    uname              = session['username']
    gameDict,result    = retrieve_game(_id)

    data = {'username': gameDict['name'], 'pet_name': gameDict['pet'], 'pet_age': gameDict['age'], 'time_elapsed': gameDict['timer']}
    # Return the data in JSON format
    return data
  except:
    print('error updating data, please clear your cache returning to login page')
    return redirect('login.html', error='error updating data, please clear your cache returning to login page')




@app.route('/clear')
def clear_session():
    session.clear()
    return 'Session cleared!'



#------ AUTO RUN

# run the app
if __name__ == '__main__':
  app.run()
  #socketio.run(app)
