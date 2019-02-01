"""Webserver."""
from aiohttp import web
from pyhassbian.manager import Manager
from pyhassbian.serverfiles import static


async def html(request):
    """Serve a HTML site."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = static.STYLE
    version = 96
    content += static.HEADER.format(version=version, previous=95, next=97)

    content += '<main>'

    suites = await get_data()

    for suite in suites:
        comp = suite

        doclink = 'doclink'
        filename = "/opt/hassbian/suites/{}.sh".format(suite)
        with open(filename, 'r') as myfile:
            shortdesc = myfile.read().replace('\n', ' ')
            shortdesc = shortdesc.split('echo "')[1].split('"')[0]
        content += static.CARD.format(
            title=comp, content=shortdesc, docs=doclink)

    content += '</main>'
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")

async def log(request):
    """Serve a HTML site."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = static.STYLE
    version = 96
    content += static.HEADER.format(version=version, previous=95, next=97)

    content += '<main>'

    lastlog = await get_log()
    lastlog = lastlog.replace('\n', '</br>')

    content = static.CARD.format(title='log', content=lastlog, docs='doclink')

    content += '</main>'
    content += static.FOOTER
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

def run_server():
    """Run the server."""
    app = web.Application()
    app.router.add_route('GET', r'/', html, name='html')
    app.router.add_route('GET', r'/log', html, name='log')
    app.router.add_route('GET', r'/json', json, name='json')
    web.run_app(app, port=9999)
