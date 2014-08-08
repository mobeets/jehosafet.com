import os.path
 
import cherrypy
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

import conf
from apps import elsewhere

# FULL_ICON_URL = '0.0.0.0:5000/static/elsewhere-icons'
# FULL_ICON_URL = 'http://thu-jehosafet-staging.herokuapp.com/static/elsewhere-icons'
FULL_ICON_URL = 'http://www.jehosafet.com/static/elsewhere-icons'
CONTACT = 'Contact me <a href="https://twitter.com/jehosafet" target="_blank">@jehosafet</a>.'
HEROKU_URL = lambda key: "http://{0}.herokuapp.com".format(key)

class Root(object):
    @cherrypy.expose
    def index(self):
        tmp = lookup.get_template('index.html')
        return tmp.render(title='thu-jehosafet', icon_key='jehosafet', full_icon_url=FULL_ICON_URL)

    @cherrypy.expose
    def default(self, *data):
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def story_fork(self, *data):
        raise cherrypy.HTTPRedirect(HEROKU_URL('story-fork'))

    @cherrypy.expose
    def booklet_helper(self, *data):
        raise cherrypy.HTTPRedirect(HEROKU_URL('pdf-page-orderer'))

    @cherrypy.expose
    def blog_word_counts(self, *data):
        raise cherrypy.HTTPRedirect(HEROKU_URL("blog-word-counts"))

    @cherrypy.expose
    def morse_news(self, *data):
        raise cherrypy.HTTPRedirect(HEROKU_URL("morse-news"))

    @cherrypy.expose
    def unfulfilled(self, *tmp):
        return cherrypy.tree.apps['/elsewhere'].root.item('unfulfilled')

    @cherrypy.expose
    def colophon(self, *data):
        tmp = lookup.get_template('colophon.html')
        return tmp.render(title='colophon', contact=CONTACT, icon_key='jehosafet', full_icon_url=FULL_ICON_URL)

    @cherrypy.expose
    def cookies(self, *data):
        tmp = lookup.get_template('cookie_helper.html')
        return tmp.render(title='Chocolate chip cookies', icon_key='cookie-helper', full_icon_url=FULL_ICON_URL)

    @cherrypy.expose
    def list_2013_misc(self, *data):
        tmp = lookup.get_template('2013-list-misc.html')
        return tmp.render(title='2013: Seen, Tried, or Tasted', icon_key='2013-list-misc', full_icon_url=FULL_ICON_URL)

    @cherrypy.expose
    def nfl_kickoffs(self, *data):
        tmp = lookup.get_template('nfl-kickoffs.html')
        return tmp.render(title='Kickoffs and returns from 2002 - 2012', icon_key='nfl-kickoffs', full_icon_url=FULL_ICON_URL)

    @cherrypy.expose
    def hive(self, *data):
        tmp = lookup.get_template('hive.html')
        return tmp.render(title='Hive', icon_key='hive', full_icon_url=FULL_ICON_URL)

    @cherrypy.expose
    def either_way(self, *data):
        tmp = lookup.get_template('either-way.html')
        return tmp.render(title='Either way, he thinks', icon_key='either-way', full_icon_url=FULL_ICON_URL)
 
def main():
    cherrypy.config.update(conf.settings)
    root_app = cherrypy.tree.mount(Root(), '/', conf.root_settings)
    elsewhere_app = elsewhere.main(conf.elsewhere_settings, CONTACT, FULL_ICON_URL)
    cherrypy.tree.mount(elsewhere_app, '/elsewhere', {})
    root_app.merge(conf.settings)
    if hasattr(cherrypy.engine, "signal_handler"):
        cherrypy.engine.signal_handler.subscribe()
    if hasattr(cherrypy.engine, "console_control_handler"):
        cherrypy.engine.console_control_handler.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
