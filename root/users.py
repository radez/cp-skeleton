import cherrypy

from root.authentication import auth_role
from model.user import User
from root.base import Base


class AdminUsers(Base):

    _cp_config = {
        'auth.require': [auth_role('admin')]
    }

    @cherrypy.expose
    @cherrypy.tools.template(template='admin_users.html')
    def index(self):
        users = self.db.query(User).all()
        return self.j2render(session=cherrypy.session,
                             request=cherrypy.request,
                             users=users)


class UsersWebService(Base):

    _cp_config = {
        'auth.require': [auth_role('admin')]
    }
