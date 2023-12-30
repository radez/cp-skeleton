# -*- coding: utf-8 -*-
import cherrypy

__all__ = ['Jinja2Tool']


class Jinja2Tool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self._bind_j2render,
                               priority=10)

    def _bind_j2render(self, template=None):
        if template:
            template = cherrypy.engine.publish("lookup-template", template).pop()
            cherrypy.request.j2render = template.render
