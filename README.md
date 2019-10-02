
# Recast.AI Conversation Manager
> A user-friendly way to manage your recast.ai bots :robot: !
<p align="center">
  <img src="https://media.giphy.com/media/idpT1kuCaGz1o0b1DF/giphy.gif" width="400"/> 
</p>

Recast.AI Conversation Manager is a web platform that kind of complements the features offered by Recast.AI (SAP Conversational AI). It centralizes the conversations received from the different channels connected to the chatbot and instantly displays them in a single page. One of the main features it offers is the possibility to toggle on and off the bot mode temporarly in order to directly reply to users from the platform when needed. It also allows brodcasting messages to a group of users and adding new managers that will be able to take control on some users' bot conversations.

This project has been conducted as part of my summer internship project in July 2018. 


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


