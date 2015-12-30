# coding: utf-8

from . import auth


@auth.route('/')
def index():
    return 'ololo'