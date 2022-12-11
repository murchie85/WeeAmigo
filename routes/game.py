from flask import Flask, render_template, session, request, redirect
from tableFunctions import *
from gameFunctions  import *
from threading import Thread



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
      # TODO UPDATE CODE SO THE USER CHANGES ARE UPDATED  OTHERWISE EACH REFRESH WILL RESET OBJ VALUES

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

