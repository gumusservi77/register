import hashlib

import os

from requests import Session 

# Create a state token to prevent request forgery.
# Store it in the session for later validation.
state = hashlib.sha256(os.urandom(1024)).hexdigest()
# Session['state'] = state
# Set the client ID, token state, and application name in the HTML while
# # serving it.
# response = responses(CLIENT_ID='608464615033-ken7kqeb20k31a4mgktcjm7lu03v1pe9.apps.googleusercontent.com',STATE=state,APPLICATION_NAME='register app')
print (state)