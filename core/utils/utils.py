#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json
from shutil import copy
from core.config.settings import logger
import subprocess
import types

#from pprint import pprint
from core.config import settings


class Utils:
    """class Util"""

    def __str__(self):
        return 'Util'

    def __init__(self):
        pass

    @staticmethod
    def get_full_path_to_info_by_sentense(sentense):
        p = re.compile('[\s+/:()<>|?*]|(\\\)')
        path = p.sub('/', sentense)
        if path.startswith('/'):
            path = path[1:]
        #create directories recursively
        logger.info(path)
        logger.info(settings.APP_DIRS['audio_dir'] + path)
        if not os.path.isdir(settings.APP_DIRS['audio_dir'] + path):
            os.makedirs(os.path.join(settings.APP_DIRS['audio_dir'], path))
        return settings.APP_DIRS['audio_dir'] + path

    def get_full_path_to_module_by_request(self, request):
        """ Get path to brain module by requested text,
        if no such module exists create default one """
        path = self.convert_text_to_path(request)
        #create directories recursively
        #logger.info( settings.APP_DIRS['brain_modules_dir'])
        #logger.info(path)
        if not os.path.isdir(settings.APP_DIRS['brain_modules_dir'] + path):
            os.makedirs(os.path.join(settings.APP_DIRS['brain_modules_dir'] + path))
        return settings.APP_DIRS['brain_modules_dir'] + path

    @staticmethod
    def convert_text_to_path(request):
        """docstring for convert_text_to_path"""
        request = request.strip()
        list = request.split()
        if len(list) > 1:
            p = re.compile('[\s+/:()<>|?*]|(\\\)')
            path = p.sub('/', request)
        elif len(list) == 1:
            path = request

        if path.startswith('/'):
            path = path[1:]
        return path

    @staticmethod
    def get_rel_path_to_module_by_request(request):
        """ Get rel to brain module by requested text,
        if no such module exists create default one """
        request = request.strip()
        list = request.split()
        if len(list) > 1:
            p = re.compile('[\s+/:()<>|?*]|(\\\)')
            path = p.sub('.', request)
        elif len(list) == 1:
            path = request

        return path

    @staticmethod
    def load_file_json_info(path):
        """Load json file which contains detailed
        information about the audio file"""
        info = None
        try:
            json_data = open(path + '/info.json')
            info = json.load(json_data)
            json_data.close()
        except Exception as e:
            logger.exception(e)

        return info

    @staticmethod
    def get_file_extension(fname):
        """docstring for get_file_extension"""
        if fname:
            extp = fname.split('.')
            return extp[-1]

    @classmethod
    def download_audio_resource(self, link_to_audio, sentense):
        import urllib as urllib
        ext = self.get_file_extension(link_to_audio)
        dst = self.get_full_path_to_info_by_sentense(sentense)
        try:
            file = urllib.urlopen(link_to_audio)
            output = open(dst + '/audio.' + ext, 'wb')
            output.write(file.read())
            output.close()
        except Exception, e:
            logger.exception(e)
        return dst

    @classmethod
    def save_file_json_info(self, sentense, info):
        dst = self.get_full_path_to_info_by_sentense(sentense)
        output = open(dst + '/info.json', 'wb')
        info = json.dumps(info)
        output.write(info)
        output.close()
        return True

    @staticmethod
    def copy_default_reaction_files(dst):
        """copy default reaction files into new directory"""
        src = settings.APP_DIRS['brain_modules_dir'] + '/_reaction/reaction.py'
        copy(src, dst)
        src = settings.APP_DIRS['brain_modules_dir'] + '/_reaction/__init__.py'
        copy(src, dst)
        #copytree(src, dst)
        return dst

    @staticmethod
    def clean_input_audio_dir():
        os.system('rm -f ' + settings.APP_DIRS['tmp_input_audio_dir'] + '*.wav ')
        os.system('rm -f ' + settings.APP_DIRS['tmp_input_audio_dir'] + '*.flac ')


def parse_file(path_list, regex_list):
    if not isinstance(path_list, (types.ListType, types.TupleType)):
        path_list = [path_list]

    if not isinstance(regex_list, (types.ListType, types.TupleType)):
        regex_list = [regex_list]

    lines = []
    for path in path_list:
        try:
            file = open(path, 'r')
            lines.extend(file.readlines())
            file.close()
        except IOError as e:
            logger.exception(e)

    ret = {}
    for line in lines:
        for regex in regex_list:
            match = regex.match(line)
            if match:
                for k, v in match.groupdict().iteritems():
                    ov = ret.get(k, v)
                    if k in ret:
                        ov.append(v)
                    else:
                        ov = [ov]
                    ret[k] = ov

    return ret


def process_by_pipe(process_info):
    p = subprocess.Popen(process_info, stdout=subprocess.PIPE, close_fds=True)
    return p.communicate()

def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen",
        ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty",
                "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
