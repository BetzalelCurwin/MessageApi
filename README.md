# MessageApi
### important 
use endpoint /login in order to recieve a access token and be allowed access to the rest of the api  
if not logged in api will not permit access

# Endpoints  
- **/login** : accepts a post request with user email and returns access token
- **/message** : accepts a post request with message data, creates and returns message  
- **/messages** : returns all messages of the current user  
- **/messages/unread** : returns all unread messages of current user  
- **/messages/<message_id>** : accepts a get or delete request and returns or deletes message with id accordingly 
