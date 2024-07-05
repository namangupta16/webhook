## Set up in local

install mongodb
start the mongo server

connect ngrok string in webhook ( create a free ngrok url for adding a webhook as git will not take the localhost link )

## Update the Webhook URL

Go to your GitHub repository settings.
Add a new webhook with the following details:
Payload URL: http://<random-string>.ngrok.io/webhook
Content type: application/json
Events: Select individual events for Push, Pull Request, and Merge.

## Run the Application

python app.py

# In a new terminal, start ngrok to expose port 5000
ngrok http 5000

## adding comment for testing
## adding line2
## adding new line 
## testing123
## changes done