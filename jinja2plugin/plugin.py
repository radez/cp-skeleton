# -*- coding: utf-8 -*-
from cherrypy.process import plugins
from jinja2 import Environment, FileSystemLoader

__all__ = ['Jinja2Plugin']


class Jinja2Plugin(plugins.SimplePlugin):
    """A WSPBus plugin that manages Jinja2 templates"""

    def __init__(self, bus, templates):
        plugins.SimplePlugin.__init__(self, bus)
        self.bus.subscribe("lookup-template", self.get_template)
        self.env = Environment(loader=FileSystemLoader(templates))

    def start(self):
        """
        Called when the engine starts.
        """
        self.bus.log('Setting up Jinja2 resources')

    def stop(self):
        """
        Called when the engine stops.
        """
        self.bus.log('Freeing up Jinja2 resources')
        self.bus.unsubscribe("lookup-template", self.get_template)

    def get_template(self, name):
        """
        Returns Jinja2's template by name.
        Used as follow:
        >>> template = cherrypy.engine.publish('lookup-template', 'index.html').pop()
        """
        return self.env.get_template(name)

    def register_filter(self, name, func):
        self.env.filters[name] = func
