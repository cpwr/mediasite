from . import api


@api.route('/ololo')
def index():
    return 'ololo'
