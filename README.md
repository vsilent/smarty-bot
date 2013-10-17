smarty-bot
==========

Smarty-bot is a personal bot which is aimed to keep well organized scripts and execute them easy.

It is also for those who just started to learn programming in Python.<br>
For now it is just a very simple chat bot which can interpret some natural language commands into python script execution.
In the future it is going to be more than just a chat bot but transform natural language commands into real actions ( turn on lights, making coffee :) ) . <br>

This is not a ready for use product, it is still under development!<br><br>


Some more detailed info can be found at http://smarty-bot.com in russian language.<br>

For more questions write to info at smarty-bot.com


Installation
===========

1. Register a new account for you bot at gmail.com, for example  mysuperbot@gmail.com
2. Create mysql database
3. Configure core/config.settings.py
4. Create database structure:  <code>python core/people/person.py</code>

Run app:   <code>python core/init.py</code>

Login to your personal gtalk account and find bot's gtalk contact and add it.
Now you can say hi to it


Creating of a reaction
===========

It's easy,  just tell to bot  create a new reaction "say hello to me".
Bot will create a new script and place it under core/brain/say/hello/to/me/reaction.py
where you can add any python code you want.

Next time say  " say hello to me" and your function will be executed
