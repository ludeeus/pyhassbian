"""Webserver."""
import os
from aiohttp import web
from pyhassbian.manager import Manager
from pyhassbian.generated import generated

DIRPATH = os.path.dirname(os.path.realpath(__file__))

SUITES = ['appdaemon',
          'cloud9',
          'fail2ban',
          'hassbian-script',
          'hassbian',
          'homeassistant',
          'homebridge',
          'hue',
          'libcec',
          'manager',
          'mosquitto',
          'razberry',
          'samba',
          'tradfri',
          'webterminal',
          'zigbee2mqtt']


async def html(request):
    """Serve a HTML site."""
    content = generated.STYLE
    content += generated.HEADER

    content += '<main class="suites">'

    suites = await get_data()

    for suite in suites:
        if suite in SUITES:
            installed = Manager(suite=suite).suite_installed()
            if installed or suite in ['homeassistant', 'hassbian-script', 'hassbian']:
                title = "{} (installed)".format(suite)
            else:
                title = suite
            filename = "/opt/hassbian/suites/{}.sh".format(suite)
            with open(filename, 'r') as myfile:
                myfile = myfile.read().replace('\n', '')
                myfile = myfile.replace('\\n', '').replace('printf ', '')
                myfile = myfile.replace('\\', '')
                shortdesc = myfile.split('show-short-info {')[1].split('}')[0]
                shortdesc = shortdesc.replace('echo "', '').replace('"', '')
            content += generated.CARD.format(
                title=title, content=shortdesc, more=suite)

    content += '</main>'
    return web.Response(body=content, content_type="text/html")


async def suiteview(request):
    """Serve a HTML site."""
    suite = request.match_info['suite']
    has_upgrade = False
    has_install = False
    has_remove = False

    buttons = ''

    docs = "https://github.com/home-assistant/hassbian-scripts/blob/master/"
    if suite == 'hassbian-script':
        docs += "docs/hassbian_config.md"
    else:
        docs += "docs/{}.md".format(suite)

    content = generated.STYLE
    content += generated.HEADER

    content += '<main class="suite">'

    filename = "/opt/hassbian/suites/{}.sh".format(suite)
    with open(filename, 'r') as myfile:
        myfile = myfile.read().replace('\n', '</br>')
        myfile = myfile.replace('\\n', '').replace('printf ', '')
        myfile = myfile.replace('\\', '')

        if '-install-package' in myfile:
            has_install = True
        if '-upgrade-package' in myfile:
            has_upgrade = True
        if '-remove-package' in myfile:
            has_remove = True

        shortdesc = myfile.split('show-short-info {')[1].split('}')[0]
        shortdesc = shortdesc.replace('echo "', '').replace('"', '')

        longdesc = myfile.split('show-long-info {')[1].split('}')[0]
        longdesc = longdesc.replace('echo "', '').replace('"', '')

        if longdesc == shortdesc:
            longdesc = ''

    installed = Manager(suite=suite).suite_installed()

    if installed or suite in ['homeassistant', 'hassbian-script', 'hassbian']:
        title = "{} (installed)".format(suite)
    else:
        title = suite

    body = shortdesc
    body += '</br>'
    body += longdesc

    if has_install:
        if suite != 'homebridge':
            buttons += '<a href="/{}/install" class="install">Install</a>'.format(suite)
    if installed or suite in ['homeassistant', 'hassbian-script', 'hassbian']:
        if has_upgrade:
            buttons += '<a href="/{}/upgrade" class="upgrade">Upgrade</a>'.format(suite)
        if has_remove:
            buttons += '<a href="/{}/remove" class="remove">Remove</a>'.format(suite)

    buttons += '<a href="{}" target="_blank">Documentation</a>'.format(docs)

    content += generated.SUITE.format(
        title=title, content=body, buttons=buttons)
    content += '<div class="loader"></div>'
    content += '</main>'
    return web.Response(body=content, content_type="text/html")


async def log(request):
    """Serve a HTML site."""
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


async def install(request):
    """Install suite"""
    suite = request.match_info['suite']
    Manager(suite=suite, mode='install').manage_suite()
    raise web.HTTPFound('/' + suite)


async def upgrade(request):
    """upgrade suite"""
    suite = request.match_info['suite']
    if suite == 'hassbian':
        Manager().os_upgrade()
    else:
        Manager(suite=suite, mode='upgrade').manage_suite()
    raise web.HTTPFound('/' + suite)


async def remove(request):
    """remove suite"""
    suite = request.match_info['suite']
    Manager(suite=suite, mode='remove').manage_suite()
    raise web.HTTPFound('/' + suite)


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
    app.router.add_route('GET', r'/{suite}/install', install, name='install')
    app.router.add_route('GET', r'/{suite}/upgrade', upgrade, name='upgrade')
    app.router.add_route('GET', r'/{suite}/remove', remove, name='remove')
    app.router.add_static('/static/', path=str(DIRPATH + '/static/'))
    web.run_app(app, port=port)
