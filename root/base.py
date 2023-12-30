import cherrypy


class Base(object):

    @property
    def db(self):
        return cherrypy.request.db

    def j2render(self, **kwargs):
        return cherrypy.request.j2render(
            session = cherrypy.session,
            request = cherrypy.request,
            **kwargs)
