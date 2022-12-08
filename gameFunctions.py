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

