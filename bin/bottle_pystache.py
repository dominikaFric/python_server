import functools
import threading

import bottle

__all__ = ['PystacheTemplate', 'mustache_view', 'view', 'mustache_template',
    'template']

class PystacheTemplate(bottle.BaseTemplate):
    ''' Pystache is a Python Mustache implementation.
        Set `View.template_extension` to be able to use partials,
        because partial calls are not handled by Bottle and Pystache works
        with only one extension, defined as `mustache` by default.
    '''

    try:
        extensions = bottle.BaseTemplate.extensions
    except AttributeError:
        # Bottle had a misspelling in BaseTemplate.
        # It is fixed in Bottle v0.10.
        extensions = bottle.BaseTemplate.extentions
    extensions.insert(0, 'mustache')

    def __init__(self, source=None, name=None, lookup=[], encoding='utf8',
            layout=None, **settings):
        if layout:
            self.layout = layout
        super(PystacheTemplate, self).__init__(source=source, name=name,
                lookup=lookup, encoding=encoding, **settings)

    def prepare(self, **options):
        from pystache import Renderer
        self.context = threading.local()
        self.context.vars = {}
        if hasattr(self, "layout"):
            self.layout_filename = self.search(self.layout, self.lookup)
        self.tpl = Renderer(search_dirs=self.lookup,
                file_encoding=self.encoding, string_encoding=self.encoding,
                **options)

    def render(self, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)
        kwargs.update(self.defaults)
        if hasattr(self, "layout"):
            partial = self.tpl.render_path(self.filename, **kwargs)
            kwargs.update({"yield": partial})
            out = self.tpl.render_path(self.layout_filename, **kwargs)
        else:
            out = self.tpl.render_path(self.filename, **kwargs)
        return out

def view(tpl_name, layout=None):
    if layout:
        return bottle.view(tpl_name, template_adapter=PystacheTemplate,
                template_settings={"layout": layout})
    else:
        return bottle.view(tpl_name, template_adapter=PystacheTemplate)

def template(tpl_name, layout=None, *args, **kwargs):
    if layout:
        return bottle.template(tpl_name, template_adapter=PystacheTemplate,
                template_settings={"layout": layout}, *args, **kwargs)
    else:
        return bottle.template(tpl_name, template_adapter=PystacheTemplate,
                *args, **kwargs)

mustache_template = template
mustache_view = view

