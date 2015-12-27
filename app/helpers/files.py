# coding: utf-8
import config


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_FILE_EXTENSIONS
