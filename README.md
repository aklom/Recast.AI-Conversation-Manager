
# Recast.AI Conversation Manager
A user-friendly way to manage your recast.ai chatbots :robot: !

<p align="center">
  <img src="https://media.giphy.com/media/U4402tXqtkOG9gmBpY/giphy.gif" width="400"/> 
</p>


Recast.AI Conversation Manager is a web platform that complements the features offered by Recast.AI (SAP Conversational AI). It centralizes the conversations received from the different channels connected to the chatbot and instantly displays them in a single page. 

One of the main features it offers is the possibility to toggle on and off the bot mode temporarly in order to directly reply to users from the platform when needed. It also allows brodcasting messages to a group of users and adding new managers that will be able to take control on some users' bot conversations.


## Running locally
### Python environment

Set up Python environment:

```shell
$ pipenv install
```

To create a virtual environment you just execute the `$ pipenv shell`.

### Setup Pusher 
Create a Pusher account and provide your `APP_ID`, `APP_KEY` and `APP_SECRET` in the `src/utils.py` file.

### Setup a ngrok tunnel
Create a tunnel with `ngrok` to connect the API to Recast.AI: 

```
$ ngrok http 5050
``` 
NB: This link is only available for 8 hours, so you need to change it in order to keep using the app properly.

### Run the app 
```
$ python run.py
``` 


## Recast.AI Configuration

1. Fork this template-bot on recast: https://cai.tools.sap/aklom/template-conversation-manager/

2. Update the Bot Builder URL under the Settings tab by providing your ngrok link followed by `/api`
<p align="center">
  <img src="https://imgur.com/TxXw5t5.png" width="400"/> 
</p>

3. In all the available skills (and in the future skills you're about to develop), under the Actions tab, replace the Bot-name in the headers of the `/update` and `/fallback` webhooks by your bot's name. You can save this headers as a template to easily replace it in all the remaining skills. 

<p align="center">
  <img src="https://imgur.com/hguwFD6.png" width="600"/> 
</p>


## Create an account and get started !

### Sign up 
You can create an account by providing your bot's name and tokens that you will find under the Settings tab in your Recast.AI account (https://cai.tools.sap).
<p align="center">
  <img src="https://imgur.com/RHDdmVI.png" width="500"/> 
</p>

### Inbox 
Once a user sends you a message from any channel connected to your bot (and if you've done all the configuration part right), it will instantly appear in the Inbox page. You can click on Inspect to switch off the bot mode on that user and contact him. You will also find some information about the user, like his name or phone number, that has been collected from the bot's questions. This will allow you to easily reach him if the problem needs a phone call for example. 
<p align="center">
  <img src="https://imgur.com/k6Ilmm2.png" width="500"/> 
    <img src="https://imgur.com/3iaITSX.png" width="500"/> 
</p>

### Groups 

You can create groups of users to be able to easily send them collective messages through the Broadcast feature. It may be helpful for marketing needs like announcing a new feature or event!
<p align="center">
  <img src="https://imgur.com/Y9ns4wR.png" width="500"/> 
</p>


### Add managers  
In the Settings tab, you can add new managers that will be able to answer a group of users you will address to them. They will have access to the platform with a login and password you define, and that way, you don't need to share with them your tokens. 
<p align="center">
  <img src="https://imgur.com/rCfquiw.png" width="500"/> 
</p>

### Have fun creating and managing chatbots ! :-) 


