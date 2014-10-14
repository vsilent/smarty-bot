SmartyBot
==========

SmartyBot is a xmpp (gtalk) bot written in python plus 0MQ lib. 
<br>


It is also for those who just started to learn programming in Python.<br>
For now it is just a very simple chat bot which can execute natural language commands.
In the future it is going to be more than just a chat bot but execute natural language commands into real actions ( turn on lights, make coffee, open door, remind me etc. ) . <br>
Plugins of other python bots out there can be imported easily and be organized nicely.





Demo
===========

Add webdirect.bot @t gmail.com  to your test hangouts account, and write a "hello". ( No spam is quaranteed )



Installation
===========

Install libs ( Ubuntu ) :

<code>
sudo apt-get install python-dev libsdl1.2-dev libcurl4-gnutls-dev <br>
python-dnspython libxslt1-dev libxml2-dev swig portaudio19-dev libmysqlclient-dev<br>
python-m2crypto libffi-dev dict libssl-dev
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

More details at http://www.smartybot.com but in russian language only, yet.<br>

