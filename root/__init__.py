import cherrypy

from model.code import Code
from model.notification import Notification
from root.authentication import AuthController, require, auth_role
from root.base import Base
from root.users import AdminUsers, UsersWebService


class Admin(Base):

    users = AdminUsers()

    @cherrypy.expose
    @require(auth_role('admin'))
    @cherrypy.tools.template(template='admin_notifications.html')
    def notifications(self):
        notifications = self.db.query(Notification).all()

        return self.j2render(notifications=notifications)

    @cherrypy.expose
    @require(auth_role('admin'))
    @cherrypy.tools.template(template='admin_codes.html')
    def codes(self):
        codes = self.db.query(Code).all()

        return self.j2render(codes=codes)


class WebService(Base):
    users = UsersWebService()


class Root(Base):

    auth = AuthController()
    ws = WebService()
    admin = Admin()

    @require()
    @cherrypy.expose
    @cherrypy.tools.template(template='index.html')
    def index(self):
        return self.j2render()

    @cherrypy.expose
    @cherrypy.tools.template(template='modal_example.html')
    def modal(self):
        return self.j2render()
