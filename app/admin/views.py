# coding: utf-8
import os

from flask import render_template
from flask import redirect
from flask import request
from flask import send_from_directory
from flask.helpers import url_for
from werkzeug.utils import secure_filename


from . import admin
from app import app
from app.helpers.files import allowed_file


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return render_template('admin/uploads.html', filenames=filenames)


@admin.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

