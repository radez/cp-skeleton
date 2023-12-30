import cherrypy


class Base(object):

    @property
    def db(self):
        return cherrypy.request.db

    @property
    def j2render(self):
        return cherrypy.request.j2render
