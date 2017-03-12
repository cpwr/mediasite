import os

import aiohttp_jinja2

from werkzeug.utils import secure_filename

from app.lib.file import allowed_file


@aiohttp_jinja2.template('index.html')
def index(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('charts.html')
def charts(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('blank-page.html')
def blank_page(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('tables.html')
def tables(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('forms.html')
def forms(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('bootstrap-elements.html')
def bootstrap_elements(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('bootstrap-grid.html')
def bootstrap_grid(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('index-rtl.html')
def index_rtl(request):
    return {
        'app': request.app,
    }


@aiohttp_jinja2.template('uploads.html')
def upload(request):
    uploaded_files = request.files.getlist("file[]")
    filenames = list()
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(request.app['upload_folder'], filename))
            filenames.append(filename)
    return {
        'app': request.app,
        'filenames': filenames,
    }
