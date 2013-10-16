#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
"""
Data sort bot - should check unsorted requests and complete structured tables

"""


def is_email(string):
    """docstring for checkIsEmail"""
    return re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", string)
