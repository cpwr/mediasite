import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
def index(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


@aiohttp_jinja2.template('portfolio.html')
def portfolio(request):
    return {}


@aiohttp_jinja2.template('contacts.html')
def contacts(request):
    return {}
