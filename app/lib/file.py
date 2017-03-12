import os
import re
import mimetypes

from collections import namedtuple

from aiohttp import web

from app.lib.helpers import (
    http400,
    http404,
)

DEFAULT_CONTENT_TYPE = 'application/octet-stream'
FILENAME_PARSER = re.compile(r"(?P<id>\d+)_(?P<name>.+)\.(?P<format>.+)")

ParsedFile = namedtuple('ParsedFile', [
    'original_name', 'id', 'name'
])


def parse_filename(filename: str):
    if not filename:
        return
    match = FILENAME_PARSER.match(filename)
    if match is not None:
        id, name, frmt = match.groups()
        return ParsedFile(
            "{}_{}.{}".format(id, name, frmt),
            id,
            "{}.{}".format(name, frmt),
        )


def get_cache_headers():
    return {
        "Cache-Control": "public, max-age=31536000",
        "Etag": "'CacheForever'",
        "Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"
    }


def get_no_cache_headers():
    return {
        "Cache-Control": "no-store, no-cache, max-age=0",
        "Pragma": "no-cache",
    }


def get_file_headers(file_name):
    type, _ = mimetypes.guess_type(file_name)
    headers = {
        "Content-Type": "{}"
        .format(type),
        "Content-Disposition": 'attachment;filename="{}"'
        .format(file_name),
    }
    return headers


def get_non_cached_file_headers(file_name):
    headers = get_file_headers(file_name)
    headers.update(**get_no_cache_headers())
    return headers


def get_cached_file_headers(file_name):
    headers = get_file_headers(file_name)
    headers.update(**get_cache_headers())
    return headers


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1] in {
            [
                'bmp', 'eps', 'icns', 'im', 'msp', 'pcx', 'ppm',
                'png', 'tiff', 'ico', 'jpg', 'jpeg', 'gif',
            ]
        }
    )


def file_response(name, body, source):
    if body is None:
        return http404()
    return web.Response(
        body=body,
        headers={
            'X-File-Source': source,
            **get_file_headers(name)
        }
   )

async def store_mp3_handler(request):

    reader = await request.multipart()

    # /!\ Don't forget to validate your inputs /!\

    file = await reader.next()

    filename = file.filename

    if not allowed_file(filename):
        return http400()

    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join('/media/', filename), 'wb') as f:
        while True:
            chunk = await file.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(
        text='{} sized of {} successfully stored'.format(filename, size)
    )
