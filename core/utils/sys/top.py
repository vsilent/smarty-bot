#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

pids= [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
    print open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()


