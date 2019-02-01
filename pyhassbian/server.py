"""Webserver."""
from aiohttp import web
from pyhassbian.manager import Manager
from pyhassbian.serverfiles import static


async def defaultsite(request):
    """Serve root."""
    print("Session from:", request.headers.get('X-FORWARDED-FOR', None))
    content = static.STYLE
    content += static.DEFAULT
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")

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

        pull = 'pull'
        doclink = 'doclink'

        content += static.CARD.format(pull=pull, title=comp,
                                      content='description',
                                      docs=doclink,
                                      prlink='prlink')
    content += '</main>'
    content += static.FOOTER
    return web.Response(body=content, content_type="text/html")

async def json(request):
    """Serve the response as JSON."""
    json_data = await get_data()
    if not json_data:
        return web.json_response({'error': 'No changes found.'})
    return web.json_response(json_data)


async def get_data():
    """Get version data."""
    return Manager().get_suites()

def run_server():
    """Run the server."""
    app = web.Application()
    app.router.add_route('GET', r'/', defaultsite, name='defaultsite')
    app.router.add_route('GET', r'/{version}', html, name='html')
    app.router.add_route('GET', r'/{version}/json', json, name='json')
    web.run_app(app, port=9999)
