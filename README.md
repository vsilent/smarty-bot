SmartyBot
==========

SmartyBot is a personal bot which is aimed to organize well small python scripts and execute them easy.
<br>

It is also for those who just started to learn programming in Python.<br>
For now it is just a very simple chat bot which can interpret some natural language commands into python script execution.
In the future it is going to be more than just a chat bot but transform natural language commands into real actions ( turn on lights, making coffee :) ) . <br>

This is not a ready for use product, it is still under development!<br><br>


Some more detailed info can be found at http://www.smartybot.com in russian language.<br>

For more questions write to < support at smartybot.com >


Installation
===========

Install libs ( Ubuntu ) :

<code>
sudo apt-get install python-dev libsdl1.2-dev libcurl4-gnutls-dev <br>
python-dnspython libxslt1-dev libxml2-dev swig portaudio19-dev libmysqlclient-dev<br>
python-m2crypto libffi-dev dict
</code>

if you don't have pip installed:
<code>
sudo apt-get install python-pip
</code>
<br>

<br>
Try:
<code>
pip install SmartyBot
<code>

<br>
or<br>
<br>

Setup required python libs from requirements.txt

<code>pip install -r requirements.txt</code>



1. Register a new account for you bot at gmail.com, for example  mysuperbot@gmail.com
2. Create mysql database, like: mysuperbot
3. Configure core/config/settings.py
4. Set write permissions to var directory: chmod guo+w -R core/var/log/
5. Create database structure:  <code>python core/people/person.py</code>

Run app:   <code>python core/init.py</code>

Login to your personal gtalk account and find bot's gtalk contact and add it.
Now you can say hi to it


Creating of a reaction
===========

It's easy,	just send a message to bot like: <br> <code>create a new reaction "say hello to me"</code>
Bot will create all necessary directories and place the new script
under <code>core/brain/say/hello/to/me/reaction.py</code><br>
where you can add any python code you want.

After you put your cool stuff there,
save and ask bot:  <code>say hello to me </code>
Your functionality will be executed.
