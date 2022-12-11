#------ LANDING
from flask import Flask, render_template, session, request, redirect

def index():
  print('***REDIRECTING TO LOGIN PAGE FROM INDEX')
  # If the user is not logged in, render the login form
  return render_template('login.html')

