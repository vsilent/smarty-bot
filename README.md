SmartyBot
==========

SmartyBot is a xmpp (gtalk) chat bot written in python and uses 0MQ lib.
It converts speech or chat commands into python actions.
<br>

For now it is just a very simple chat bot which can execute natural language commands.
It's more than just a chat bot it executes natural language commands into real actions 
( turn on lights, make coffee, open door, remind me etc. ) . <br>


Installation
===========

1. Register a new account for you bot at gmail.com, for example  mysuperbot@gmail.com
2. git clone https://github.com/vsilent/smarty-bot.git
3. Edit core/config/settings.py
4. Execute:  docker-compose up -d
5. Create database with command: docker exec -t smarty python core/people/person.py


Login to your personal gtalk account , find bot's gtalk contact and say hi.


Create custom reaction
===========

It's easy, just tell bot something like: <br> <code>create a new reaction "say hello to me"</code>
All necessary files will be created.
Find script under <code>core/brain/say/hello/to/me/reaction.py</code><br>
Programm your script.

Check script by saving the file and asking bot:  <code>say hello to me </code>
Your cool script will be executed.


