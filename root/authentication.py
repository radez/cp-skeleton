# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#
# https://github.com/cherrypy/tools/blob/master/AuthenticationAndAccessRestrictions
# alternate method: CAS https://github.com/cherrypy/tools/blob/master/CASAuthentication

import cherrypy
import html
import urllib

from datetime import datetime, timedelta
from sqlalchemy.exc import NoResultFound
from sqlalchemy import desc

import constants as c
from model.code import Code
from model.notification import Notification
from model.user import User
from model.user import get_user
from model.user import InvalidPassword, EmptyPassword
from root.base import Base


def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    try:
        user = get_user(cherrypy.request.db, email=username)
        user.check_password(password)  # Raises Exceptions or returns True
        return user
    except (AttributeError, InvalidPassword):
        return {'msg': u'Incorrect username or password', 'css_class': 'text-danger'}
    except EmptyPassword:
        return {'msg': u'You must change your password - Please click "Forgot Password"',
                'css_class': 'text-danger'}


def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as alist of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    # format GET params
    get_parmas = urllib.parse.quote(cherrypy.request.request_line.split()[1])
    if conditions is not None:
        username = cherrypy.session['user'].email if 'user' in cherrypy.session else None
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true orfalse
                if not condition():
                    # Send old page as from_page parameter
                    raise cherrypy.HTTPRedirect('{}/auth/login/?from_page={}'.format(cherrypy.request.script_name, get_parmas))
        else:
            # Send old page as from_page parameter
            raise cherrypy.HTTPRedirect('{}/auth/login/?from_page={}'.format(cherrypy.request.script_name, get_parmas))


cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)


def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate


# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.
def auth_role(role):
    def check():
        try:
            assert cherrypy.session
        except Exception:
            return False

        if role == 'admin':
            return cherrypy.session['user'].admin
        return False

    return check


def auth_role_(role):
    return auth_role(role)()


def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login


# These might be handy
def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for _c in conditions:
            if _c():
                return True
        return False
    return check


# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for _c in conditions:
            if not _c():
                return False
        return True
    return check


# Controller to provide login and logout actions

class AuthController(Base):

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('{}/auth/login/'.format(cherrypy.request.script_name))

    def on_login(self, user):
        """Called on successful login"""
        # set the user in the session
        cherrypy.session['user'] = user

    def on_logout(self, username):
        """Called on logout"""

    def get_loginform(self, username, msg="", from_page=cherrypy.request.script_name):
        username = html.escape(username, True)
        from_page = html.escape(from_page, True)
        return self.j2render(from_page=from_page,
                             username=username,
                             do_login=True,
                             setmessage=msg).encode('utf-8')

    @cherrypy.expose
    def su(self, suToUser=None, from_page=cherrypy.request.script_name):
        # TODO(dradez): Add logging the SUs that happen
        session = cherrypy.session
        if 'suUser' in session:
            user = get_user(self.db, user_id=session['suUser'].id)
            self.on_login(user)
            del session['suUser']
        elif suToUser and session and session['user'].admin:
            user = get_user(self.db, email=suToUser)
            session['suUser'] = session['user']
            self.on_login(user)
        raise cherrypy.HTTPRedirect(from_page or cherrypy.request.script_name or '/')

    @cherrypy.expose
    @cherrypy.tools.template(template='login.html')
    def login(self, username=None, password=None, reset=False, from_page=cherrypy.request.script_name):
        msg = ''
        if username is None or password is None:
            if reset:
                msg = {'msg': 'Password has been reset'}
            return self.get_loginform("", msg, from_page=from_page)

        result = check_credentials(username, password)
        if type(result) is User:
            cherrypy.session.regenerate()
            self.on_login(result)
            raise cherrypy.HTTPRedirect(from_page or cherrypy.request.script_name or '/')
        else:
            return self.get_loginform(username, result, from_page)

    @cherrypy.expose
    def logout(self, from_page=cherrypy.request.script_name):
        if 'user' in cherrypy.session:
            username = cherrypy.session['user'].email
            del cherrypy.session['user']
            if 'suUser' in cherrypy.session:
                del cherrypy.session['suUser']
            cherrypy.session.regenerate()
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or cherrypy.request.script_name or '/')

    @cherrypy.expose
    @cherrypy.tools.template(template='forgot.html')
    def forgot(self, username='', code='', newpassword='', verifypassword=''):
        msg = ''
        code_id = None
        sent = False
        if username:
            user = get_user(self.db, email=username)
            if user:
                _code = self.db.query(Code).filter(Code.email == user.email,
                                                   Code.type == c.FORGOT,
                                                   Code.processed == None).order_by(desc(Code.stamp)).first()  # noqa E711
                if not (_code and _code.stamp >= datetime.now() - timedelta(minutes=10) and _code.processed is None):
                    _code = Code(type=c.FORGOT, email=username)
                    self.db.add(_code)
                code_id = _code.id
                n10n = self.db.query(Notification).filter(Notification.meta == f'{{"{c.EMAIL}": "{username}", "{c.CODE}": "{code_id}"}}').first()
                if not n10n:
                    n10n = Notification(type=c.FORGOT)
                    n10n.store_data({c.EMAIL: username, c.CODE: code_id})
                    self.db.add(n10n)
                    self.db.commit()
                msg = {'msg': 'Password reset code has been sent'}
                sent = True

        elif code and cherrypy.request.method == 'POST':
            try:
                _code = self.db.query(Code).filter(Code.id == code, Code.type == c.FORGOT).one()
                if _code.stamp >= datetime.now() - timedelta(minutes=10) and _code.processed is None:
                    user = get_user(self.db, email=_code.email)
                    if not newpassword:
                        msg = {'msg': 'Password cannot be empty', 'css_class': 'alert-warning'}
                    elif newpassword == verifypassword:
                        user.set_password(newpassword)
                        _code.process()
                        self.db.commit()
                        raise cherrypy.HTTPRedirect(f'{cherrypy.request.script_name}/auth/login/?reset=true')
                    else:
                        msg = {'msg': 'Passwords do not match', 'css_class': 'alert-warning'}
                else:
                    msg = {'msg': 'Code has expired', 'css_class': 'alert-danger'}
            except NoResultFound:
                msg = {'msg': 'Invalid code provided', 'css_class': 'alert-danger'}
        return self.j2render(username=username,
                             code=code,
                             sent=sent,
                             do_forgot=True,
                             setmessage=msg).encode('utf-8')

    @cherrypy.expose
    @cherrypy.tools.template(template='invite.html')
    def invite(self, username='', code='', firstname='', lastname='', newpassword='', verifypassword=''):
        msg = ''
        sent = False
        if code and cherrypy.request.method == 'POST':
            try:
                _code = self.db.query(Code).filter(Code.id == code, Code.type == c.FORGOT).one()
                if _code.stamp >= datetime.now() - timedelta(minutes=10) and _code.processed is None:
                    user = get_user(self.db, email=_code.email)
                    if not newpassword:
                        msg = {'msg': 'Password cannot be empty', 'css_class': 'alert-warning'}
                    elif newpassword == verifypassword:
                        user.set_password(newpassword)
                        _code.process()
                        self.db.commit()
                        raise cherrypy.HTTPRedirect(f'{cherrypy.request.script_name}/auth/login/?reset=true')
                    else:
                        msg = {'msg': 'Passwords do not match', 'css_class': 'alert-warning'}
                else:
                    msg = {'msg': 'Code has expired', 'css_class': 'alert-danger'}
            except NoResultFound:
                msg = {'msg': 'Invalid code provided', 'css_class': 'alert-danger'}
        return self.j2render(username=username,
                             code=code,
                             sent=sent,
                             do_forgot=True,
                             setmessage=msg).encode('utf-8')
# /auth/login?from_page=" /><script>alert('XSS' + document.cookie);</script><
# (URLencodet of course)
