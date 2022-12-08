# WeeAmigo


![Image of tamagochi](https://m.media-amazon.com/images/I/819ZUKGJraS._AC_SX425_.jpg)  

## CONTENTS

1. Outline
2. Jobs done
3. Features
4. Consideration


# Stuff I learned about Flask dev

- Page wont even render if something is wrong but not a python issue (check return on routes)
- Reading json from sqlite3 is still in text form. You need to jsonloads
- you can clear session with `session.clear()` but use a flag so it happens only once on load
- Debugging is hard, logs arent so clear


  
## Outline  
  
This is a web tribute to Tamagochi toys from the past where you can raise a little digital pet. 

## Jobs   

| Task  | Status |
|-------|-------|
| Basics  | Done |
| Drawings  | Incomplete |
| Mocks  | Incomplete |
| Stack Choice  | Incomplete |
  


## Bullets  
  

- User creates an account
- User Hatches an egg to get a pet
- User raises the pet over digital time 


## FEATURES

- Go for a walk
- feed me
- pet me 
- play with me
	- fetch ball
	- dancing
- Play with other pets
- Enter race competition
- Enter fighting competition

## Inspiration   
  
- Tamagochi
- Chao from Sonic Adventure 
  
  
## Considerations    
  

- Easier to code in python, but harder to integrate into a webapp. 
- FARM stack, using python, fastapi, react and MongoDB
- MERN stack, using Mongo, Express web, react and node.  
  
React probably isn't required, just a DB that can be deployed, backend logic to manage lifecycle, javascript to manage button actions and slide images, css bootstrapping to make the app mobile compatible. 

Decision: I should probably do it all in javascript, but mocking out in FARM might be easier.  



## Drawings

Happy
Sad
Speaking
Ill
Sleeping 

