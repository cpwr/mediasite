# coding: utf-8

from flask.templating import render_template
from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/portfolio')
def portfolio():
    return render_template('main/portfolio.html')


@main.route('/contacts')
def contacts():
    return render_template('main/contacts.html')
