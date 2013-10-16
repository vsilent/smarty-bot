def start_dialog(text):
    if text is None:
        text = recognize_by_google()
        if text is None:
            return

    logging.debug( "You said: " + text )
    c = Confirm(text)
    state = c.get_state( sentence=text )

    logging.debug(type(state))
    logging.debug(state)

    if(( state == 0) or (state is None)):
        sentence = 'DID YOU SAY' + text.upper() + '?'
        say(sentence)
        logging.debug('start confirm')
        listen()
        os.system('mv ' + settings.app_dirs['tmp_input_audio_dir'] + 'speech.flac' + ' ' + settings.app_dirs['tmp_input_audio_dir'] + 'last-speech.flac')
        #confirmation = recognize_by_google()
        confirmation = ask_julius()

        if (confirmation is not None) and ('yes' in confirmation.strip().lower()):
            s = 'You said %s' % confirmation
            _utils = Utils()
            path = _utils.get_full_path_to_module_by_request(text)
            #copy default reaction files
            if not os.path.isfile( path + '/reaction.py' ):
                _utils.copy_default_reaction_files( path + '/' )
            logging.debug(s)
            say('OKAY, NICE!')
            c.confirm(1)
            logging.debug('Searching for media in internet...')
            say('NOTHING FOUND.  IM TRYING TO FIND INFORMATION IN THE INTERNET!')
            link_to_audio = search_www(text)
            logging.debug(text)
            downloaded = _utils.download_audio_resource(link_to_audio, text)
            if downloaded:
                play(text)
            else:
                say("SORRY !, COULD NOT FIND, MEDIA, FILE, AT WIKI WEBSITE")
                suggest_info(text)
        elif confirmation is not None and 'no' in confirmation.strip().lower():
            say('SORRY, PLEASE, COME CLOSER, AND, REPEAT YOUR QUESTION')
        else:
            say('PLEASE ASK AGAIN')
            os.system('rm -f ' + settings.app_dirs['tmp_input_audio_dir'] + '*.wav ')
            #start dialog from begining
            #listen()
            #start_dialog()
    else:
        #already know the answer :) play it
        play(text)
        finish_dialog()

def search_www( text_to_search ):
    """docstring for search_www"""
    #small hack for searching exactly wiki or dictionary files
    json_results = search( text_to_search)
    # now grep the results and find wiki info
    if not json_results:
        say('OOPS, COULD NOT CONNECT GOOGLE')
        return False

    _wiki = Wiki()
    wiki_page_link = _wiki.find_resourse_link(json_results)

    if wiki_page_link:
        link_to_audio = _wiki.find_audio_resourse(wiki_page_link)

        info = { 'audio_external': link_to_audio
                 ,'wiki_external' : wiki_page_link
                 ,'audio_local'   : ''
               }

        #logging.debug('save json %s' % info)
        _utils = Utils()
        _utils.save_file_json_info(text_to_search, info)

        if link_to_audio:
            return link_to_audio

    return False
