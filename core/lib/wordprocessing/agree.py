#!/usr/bin/env python
# -*- coding: utf-8 -*-


def agree(text):
    """docstring for agree"""
    if text.lower() in ['y', 'yes', 'yeps', 'ok', 'true', 'sure']:
        return True
    return False
