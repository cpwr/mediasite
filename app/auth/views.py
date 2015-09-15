from . import auth


@auth.route('/')
def index():
    return 'ololo'