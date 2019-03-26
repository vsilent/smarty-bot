SmartyBot
==========

SmartyBot is a xmpp (gtalk) bot written in python and using 0MQ lib.
It converts speech commands to python actions.
<br>


It is also for those who just started to learn programming in Python.<br>
For now it is just a very simple chat bot which can execute natural language commands.
In the future it is going to be more than just a chat bot but execute natural language
commands into real actions ( turn on lights, make coffee, open door, remind me etc. ) . <br>
Plugins of other python bots out there can be imported easily and be organized nicely.


Installation
===========

1. Register a new account for you bot at gmail.com, for example  mysuperbot@gmail.com
2. git clone https://github.com/vsilent/smarty-bot.git
3. Edit core/config/settings.py
4. Execute:  docker-compose up -d

4. Set write permissions to var directory: chmod guo+w -R core/var/log/
5. Create database structure:  <code>python core/people/person.py</code>

Run app:   <code>python core/init.py</code>

Login to your personal gtalk account , find bot's gtalk contact and say hi.


Create custom reaction
===========

It's easy, just tell bot something like: <br> <code>create a new reaction "say hello to me"</code>
All necessary files will be created.
Find script under <code>core/brain/say/hello/to/me/reaction.py</code><br>
Programm your script.

Check script by saving the file and asking bot:  <code>say hello to me </code>
Your cool script will be executed.


