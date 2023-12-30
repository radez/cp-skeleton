import cherrypy
import configparser
import os

from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin
from datetime import datetime

from jinja2plugin import Jinja2Tool, Jinja2Plugin
from model import Base


DT_FORMAT = '%m/%d/%Y'
HERE = os.path.dirname(os.path.abspath(__file__))


def js_str2bool(value, default_none=True):
    return True if value == 'true' else False if value == 'false' else value if value in ('*', '-', '!') or not default_none else None


def j2_date_fromts(value, fmt=None):
    if value:
        dt = datetime.fromtimestamp(value)
        return dt.strftime(fmt) if fmt else dt
    return ''


def j2_datefmt(value, fmt='%m/%d'):
    if value:
        dt = datetime.strptime(value, DT_FORMAT) if type(value) is not datetime else value
        return dt.strftime(fmt)
    return ''


def j2_sizefmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def j2_uuidshort(uuid):
    return uuid.split('-')[0]


def parse_config(config_file):
    config = configparser.ConfigParser()
    if not config.read(config_file):
        cherrypy.log('{} not found'.format(config_file))
    return config


def setup_server(verbose=False):
    static_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'static'))
    cherrypy.config.update({'tools.staticdir.root': static_path})
    cherrypy.tools.db = SQLAlchemyTool()
    cherrypy.tools.template = Jinja2Tool()

    template_path = cherrypy.config['paths']['templates']
    url_prefix = cherrypy.config['paths']['url_prefix']
    # template_path = 'templates'
    j2_plugin = Jinja2Plugin(cherrypy.engine, templates=template_path)
    j2_plugin.subscribe()

    from root import Root, authentication
    j2_plugin.env.globals['auth_role'] = authentication.auth_role_
    j2_plugin.env.filters['date_fromts'] = j2_date_fromts
    j2_plugin.env.filters['datefmt'] = j2_datefmt
    j2_plugin.env.filters['sizefmt'] = j2_sizefmt
    j2_plugin.env.filters['uuidshort'] = j2_uuidshort
    # mount server endpoints
    cherrypy.tree.mount(Root(), url_prefix, config={
        '/': {
            'tools.sessions.on': True,
            # memory is not shared with multiple instances of cp
            # redis or memcache perferred
            'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            # 'tools.sessions.storage_class': cherrypy.lib.sessions.MemcachedSession,
            'tools.sessions.storage_path': HERE + '/sessions',
            'tools.sessions.timeout': 60,
            # 'tools.session_auth.on': True,
            # 'tools.session_auth.check_username_and_password': Authentication.check_user,
            # 'tools.session_auth.login_screen': Authentication.login_screen,
            'tools.auth.on': True,
            'tools.db.on': True,
            'tools.template.on': True,
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'img'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    })
    sqlalchemy_plugin = SQLAlchemyPlugin(
        cherrypy.engine, Base, cherrypy.config['db']['url'],
        echo=verbose, pool_recycle=1800  # 5 Hours
    )
    sqlalchemy_plugin.subscribe()
    # Uncomment if you'd like database tables to be autocreated
    # sqlalchemy_plugin.create()
