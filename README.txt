libs required from ubuntu distribution

sudo apt-get install python-dev
sudo apt-get install libsdl1.2-dev
sudo apt-get install libcurl4-gnutls-dev python-dnspython

Setup required python libs from requirements.txt
====================================================================================================

pip install -r requirements.txt

Setup database
====================================================================================================
.....

for now sqlalchemy is in use. All meta are in the core/people/person.py file
Of course a better installation script is needed


How to create a new reaction
====================================================================================================

read http://smarty-bot.com/developers
You can use core/console.py or python core/fake_request.py in development.

Todo
====================================================================================================

1. Make a help developers module
2. Make a help user module
3. Search through wikipedia API
4. Google Voice client service
5. Skype client service
6. Local speech to text recognize system (julius is used for now but not
   ready yet)
7. Suggestion a reaction when request something.
8. Twilio integration (SMS handling)
9. Linkedin integration



