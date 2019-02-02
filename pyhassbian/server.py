"""Webserver."""
from aiohttp import web
from pyhassbian.manager import Manager
from pyhassbian.generated import generated


async def html(request):
    """Serve a HTML site."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = generated.STYLE
    content += generated.HEADER

    content += '<main class="suites">'

    suites = await get_data()

    for suite in suites:
        filename = "/opt/hassbian/suites/{}.sh".format(suite)
        with open(filename, 'r') as myfile:
            shortdesc = myfile.read().replace('\n', ' ')
            shortdesc = shortdesc.split('echo "')[1].split('"')[0]
        content += generated.CARD.format(
            title=suite, content=shortdesc, more=suite)

    content += '</main>'
    return web.Response(body=content, content_type="text/html")

async def suiteview(request):
    """Serve a HTML site."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    suite = request.match_info['suite']
    content = generated.STYLE
    content += generated.HEADER

    content += '<main class="suite">'

    filename = "/opt/hassbian/suites/{}.sh".format(suite)
    with open(filename, 'r') as myfile:
        shortdesc = myfile.read().replace('\n', ' ')
        shortdesc = shortdesc.split('echo "')[1].split('"')[0]
    content += generated.CARD.format(
        title=suite, content=shortdesc, more=suite)

    content += '</main>'
    return web.Response(body=content, content_type="text/html")

async def log(request):
    """Serve a HTML site."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = generated.STYLE
    content += generated.HEADER

    content += '<main class="log">'

    lastlog = await get_log()
    lastlog = lastlog.replace('\n', '</br>')

    content += generated.LOG.format(lastlog)

    content += '</main>'
    return web.Response(body=content, content_type="text/html")

async def json(request):
    """Serve the response as JSON."""
    json_data = await get_data()
    return web.json_response(json_data)


async def get_data():
    """Get version data."""
    return Manager().get_suites()

async def get_log():
    """Get version data."""
    return Manager().log()

def run_server(port):
    """Run the server."""
    app = web.Application()
    app.router.add_route('GET', r'/', html, name='html')
    app.router.add_route('GET', r'/log', log, name='log')
    app.router.add_route('GET', r'/json', json, name='json')
    app.router.add_route('GET', r'/{suite}', suiteview, name='suiteview')
    app.router.add_static('/static/', path=str('./pyhassbian/static/'))
    web.run_app(app, port=port)
