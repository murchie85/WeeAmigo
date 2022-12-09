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
#os.environ['FLASK_SOCKETIO_SERVER_ADDRESS'] = 'http://127.0.0.1:5000'


#------ DEFINE APP

app = Flask(__name__)
socketio = SocketIO(app)
#socketio = SocketIO(app, server_address='http://127.0.0.1:5000/')



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




# Register an event handler that will be called when a client connects to the server
@socketio.on('connect')
def on_connect():
  print('****CLIENT CONNECTED')
  exit()

@socketio.on('update')
def on_update(data):
  # Handle the update event here
  print('****Received update:', data)

# Register an event handler that will be called when a client disconnects from the server
@socketio.on('disconnect')
def on_disconnect():
  print('****Client disconnected')





# Route for the game page
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
    
    # Start a timer to update the game state at regular intervals
    print('STARTING BACKGROUND SOCKET TASK')
    # Create a new thread to run the update_game_state() function
    update_game_thread = Thread(target=update_game_state, args=(gameInstance,))
    # Start the thread
    update_game_thread.start()


    return render_template('index.html', username=gameInstance.name, pet_name=gameInstance.pet, pet_age=gameInstance.age,time_elapsed=gameInstance.timer )
  else:
    return 'Something went wrong..contact the dev.'



# Function that updates the game state and sends updates to the client
def update_game_state(game_instance):
  while True:
    print('running')
    game_instance.run_game()
    print(game_instance.timer)
    print(game_instance.age)

    # Send an update to the client with the latest game state
    socketio.emit('update', {'username': game_instance.name, 'pet_name': game_instance.pet, 'pet_age': game_instance.age, 'time_elapsed': game_instance.timer})


    # Wait a short time before sending the next update
    time.sleep(1)




@app.route('/clear')
def clear_session():
    session.clear()
    return 'Session cleared!'



#------ AUTO RUN

# run the app
if __name__ == '__main__':
  #app.run()
  socketio.run(app)
