Setup required python libs from requirements.txt
====================================================================================================

pip install -r requirements.txt

Setup database
====================================================================================================

1. Type python setup/setup.py
2. Type python test/run.py.


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



What robot can do already.
====================================================================================================

1. Listen and record audio from internal microphones
2. Recognize human speech using google web services
3. Search google
4. Download media files from spoken wiki resource (currently local web-service)
5. Play audio using almost any avaliable linux console players ( mplayer )
6. Speak using speech-dispatcher espeak/festival

