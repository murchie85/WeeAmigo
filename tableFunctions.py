import sqlite3
import json
import os

def initDB():
	# Check if the database file exists
	if not os.path.exists('users.db'):
	  # Create the database file
	  print('creating users')
	  open('users.db', 'w+').close()
	  createUserTable()


def createUserTable():
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username text,password text, pet_name text, game_data JSON)")
	c.close()


def checkUserTableExists():
	try:
		# Connect to the database
		conn = sqlite3.connect('users.db')

		# Check if the users table exists, and create it if it does not
		c = conn.cursor()
		c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
		if not c.fetchone():
		  c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username text,password text, pet_name text, game_data JSON)")

		c.close()

	except Exception as e:
		# Log the error and return a 500 Internal Server Error response
		print(e)
		return "An error occurred while processing your request.", 500



def createUser(_id, username,pet_name,password,game):
	print("Called")
	try:
		# Store the user's information in the database
		conn = sqlite3.connect('users.db')

		# Create a cursor object
		cursor = conn.cursor()


		# Convert the game object to a JSON string
		game_data = json.dumps(game.to_json())
		
		print(game_data)
		print("Dumped game_data: " + str(game_data) + ' type: ' + str(type(game_data)))

		# Construct the INSERT statement with placeholders for the values
		insert_stmt = 'INSERT INTO users (id, username, pet_name, password, game_data) VALUES (?, ?, ?, ?, ?)'

		# Execute the INSERT statement, passing in the values from the form
		cursor.execute(insert_stmt, (_id, username, pet_name, password,game_data))

		# Commit the changes to the database
		conn.commit()

		# Close the connection
		conn.close()
		print("*****User created")

	except Exception as e:
		# Log the error and return a 500 Internal Server Error response
		print(e)
		return "An error occurred while processing your request.", 500


def returnUser(username, password):
  # Query the database to see if the username and password are correct
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
  user = c.fetchone()
  print("User details are ")
  print(user)
  c.close()
  return(user)



# Create a function to store the game instance in the database
def store_game(game, user_id):
	try:
		# Convert the game object to a JSON string
		game_json = json.dumps(game)

		# Connect to the database
		conn = sqlite3.connect('users.db')

		# Create a cursor object
		cursor = conn.cursor()

		# Update the game_data column in the users table with the game JSON string
		cursor.execute("UPDATE users SET game_data=? WHERE id=?", (game_json, user_id))

		# Commit the changes to the database
		conn.commit()

		# Close the connection
		conn.close()
	except Exception as e:
		# Log the error and return a 500 Internal Server Error response
		print(e)
		return "An error occurred while processing your request.", 500

# Create a function to retrieve the game instance from the database
def retrieve_game(user_id):
	try:
		# Connect to the database
		conn = sqlite3.connect('users.db')

		# Create a cursor object
		cursor = conn.cursor()

		# Retrieve the game JSON string from the users table
		cursor.execute("SELECT game_data FROM users WHERE id=?", (str(user_id)))
		game_json = cursor.fetchone()

		# GETTING JSON STRING ONLY
		game_json = game_json[0]
		
		# PRINT
		print('Game Json string' + str(game_json))
		print(type(game_json))

		# Convert the game JSON string back into a Game object
		game = json.loads(game_json)
		print("CONVERTED into game: " + str(game))

		# check if the JSON object is a dictionary (i.e. a valid JSON object)
		if not isinstance(game, dict):
			print('failed check - returning')
			return None,"FAILURE LOADING YOUR SESSION: (if not isinstance(game_json, dict)) PLEASE CONTACT THE DEV AUTHOR"


		# Close the connection
		conn.close()
		print('GAME LOADED')
		print(game)
		return game, 'success'
	except Exception as e:
		# Log the error and return a 500 Internal Server Error response
		print(e)
		return None,"An error occurred while processing your request. Please contact the dev."
