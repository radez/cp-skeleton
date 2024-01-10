#!python3
import sys
import cherrypy
import argparse

import constants as c
from config import parse_config, setup_server

# force python 3
if sys.version_info[0] <= 3 and sys.version_info[1] < 6:
    raise "Must be using Python 3.6 or greater"

# Setup Arg Parse
parser = argparse.ArgumentParser(description='CherryPy Server')
parser.add_argument('-c', '--config', default=f'{c.PROJNAME}.conf')
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('-p', '--port', default=9000, type=int)
parser.add_argument('--ssl', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true', default=False)

args = parser.parse_args()

# Merge runtime config from conf file into
# CherryPy config data structure
cfg = parse_config(args.config)
cfg = dict(cfg)
del cfg['DEFAULT']
cherrypy.config.update(cfg)

setup_server(args.verbose)
app = cherrypy.tree

def error_page_default(status, message, traceback, version):
    return f'''<html>
<head><title>{status}</title></head>
<body>
<center>
<p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p>
<h1>{status}</h1>
<p>Please contact the administrator.</p>
</center>
</body>
</html>'''

if __name__ == "__main__":
    # Start the server for development
    if args.ssl:
        cherrypy.config.update({'server.ssl_certificate': './server.crt',
                                'server.ssl_private_key': './server.key'})
    cherrypy.config.update({'server.socket_host': args.host,
                            'server.socket_port': args.port})
    # Start up CherryPy
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    # Start up for uwsgi
    cherrypy.config.update({'engine.autoreload.on': False,
                            'error_page.default': error_page_default})
    cherrypy.server.unsubscribe()
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
