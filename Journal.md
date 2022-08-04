# Fri Sep 3 

## What I have
App now will use redis to handle sessions. 
App authenticates with Spotify Oauth2 and gets token
Fetches user profile data on /users

## What I'll do
Check if I already have a session available.

Check if the token works => if not, then I have to use the refresh token to get a new one.




# Fri Aug 27

## What I have

App authenticates with Spotify Oauth2 and gets token
Fetches user profile data on /users

## what I'll do:

Clean up the code.
Save the session details on a redis database.



# Future ideas and things to do:

- Use Mongo to save the user data or to load and compare with current data
- Angular Web app to connect to the server
- Use Docker compose to install the app