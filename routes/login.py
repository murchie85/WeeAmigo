#------ LANDING
from flask import Flask, render_template, session, request, redirect
from tableFunctions import *

#------ LOGIN
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


