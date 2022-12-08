from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# database to store user credentials
user_database = {}

# pet class with timer and age parameter
class Pet:
  def __init__(self, name):
    self.name = name
    self.timer = 0
    self.age = 0

  def increment_timer(self):
    self.timer += 1
    self.age = self.timer / 3600

# game class with run_game function
class Game:
  def __init__(self, pet):
    self.pet = pet

  def run_game(self):
    self.pet.increment_timer()

# route for the home page
@app.route('/')
def home():
  return render_template('home.html')

# route for the signup page
@app.route('/signup')
def signup():
  return render_template('signup.html')

# route for the login page
@app.route('/login')
def login():
  return render_template('login.html')

# route for the game page
@app.route('/game')
def game():
  # get the pet's name from the user's input
  pet_name = request.args.get('pet_name')
  # create a new pet object
  pet = Pet(pet_name)
  # create a new game object
  game = Game(pet)
  # start the game
  game.run_game()
  return render_template('game.html', pet=pet)

# route for handling signup form submission
@app.route('/signup', methods=['POST'])
def handle_signup():
  # get the username and password from the form
  username = request.form['username']
  password = request.form['password']
  # add the username and password to the database
  user_database[username] = password
  # redirect to the login page
  return redirect(url_for('login'))

# route for handling login form submission
@app.route('/login', methods=['POST'])
def handle_login():
  # get the username and password from the form
  username = request.form['username']
  password = request.form['password']
  # check if the username and password are correct
  if username in user_database and user_database[username] == password:
    # redirect to the game page
    return redirect(url_for('game'))
  else:
    # redirect to the login page with an error message
    return redirect(url_for('login', error="Invalid username or password"))

# run the app
if __name__ == '__main__':
  app.run()
