import cherrypy
from dateutil import parser
 
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

from model import load, load_content

TITLE = 'ELSEWHERE'
class Root(object):
    def __init__(self, items, media_dir, contact_msg, full_icon_url):
        self.full_icon_url = full_icon_url
        self.contact_msg = contact_msg
        self.media_dir = media_dir
        self.items = sorted(items, key=lambda item: parser.parse(item['date']), reverse=True)
        self.categs = set([x['categ'] for x in self.items])

    def visible_items(self):
        return [item for item in self.items if item['categ'] not in ['hidden']]

    @cherrypy.expose
    def index(self):
        title = TITLE
        tmp = lookup.get_template('elsewhere.html')
        return tmp.render(title=title, full_icon_url=self.full_icon_url, icon_key='jehosafet', contact=self.contact_msg, categs=self.categs, items=self.visible_items())

    @cherrypy.expose
    def item(self, key):
        x = [y for y in self.items if y['key'] == key]
        if not x:
            raise cherrypy.HTTPRedirect("/")
        x = x[0]
        title = x['name']
        filetype = x['kind'].lower()
        if not filetype:
            raise cherrypy.HTTPRedirect("/")
        content = load_content(self.media_dir, key, filetype)
        tmp = lookup.get_template('elsewhere-content.html')
        return tmp.render(title=title, full_icon_url=self.full_icon_url, icon_key=key, contact=self.contact_msg, content=content)

def main(settings, contact_msg, full_icon_url):
    media_dir = settings['media_dir']
    items = load(settings['data_dir'])
    return Root(items, media_dir, contact_msg, full_icon_url)
