import os.path
from collections import namedtuple

import cherrypy
from unidecode import unidecode
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

Section = namedtuple('Section', 'name statements')
Location = namedtuple('Location', 'dt name')
Interview = namedtuple('Interview', 'number subject intro sections locations')

FILEPRE = 'unfulfilled-'
FILEPOST = '.interview'
OUTRO_FILE = 'end_graph.txt'
class Root(object):
    def __init__(self, media_dir, media_path, full_icon_url):
        self.media_dir = media_dir
        self.media_path = media_path
        self.full_icon_url = full_icon_url
        self.issues = self.load_issues()

    def make_title(self, interview):
        return 'Unfulfilled #{0}'.format(interview.number)

    def photo_title(self, interview):
        path = 'unfulfilled-{0}.png'.format(interview.number)
        if not os.path.exists(os.path.join(self.media_path, path)):
            return ''
        return '/' + self.media_dir + '/' + path

    def default_outro(self):
        path = os.path.join(self.media_path, OUTRO_FILE)
        return open(path).read()

    @cherrypy.expose
    def index(self, *tmp):
        return cherrypy.tree.apps['/elsewhere'].root.item('unfulfilled')

    def load_issues(self):
        ds = []
        still_got_it = True
        i = 1
        while still_got_it:
            issue = self.load_issue(i)
            if issue:
                ds.append(issue)
            else:
                still_got_it = False
            i += 1
        return ds

    def load_issue(self, number):
        infile = os.path.join(self.media_path, FILEPRE + str(number) + FILEPOST)
        return self.load_interview(infile, number)
 
    @cherrypy.expose
    def issue(self, *tmp, **data):
        if len(tmp) != 1:
            raise cherrypy.HTTPRedirect('/unfulfilled')
        number = tmp[0]
        if not str(number).isdigit() or int(number)-1 not in range(len(self.issues)):
            raise cherrypy.HTTPRedirect('/unfulfilled')
        x = self.issues[int(number)-1]
        tmp = lookup.get_template('interview.html')
        outro = self.default_outro()
        drawing = self.photo_title(x)
        return tmp.render(title=self.make_title(x), icon_key='unfulfilled', full_icon_url=self.full_icon_url, drawing=drawing, subject=x.subject, intro=x.intro, sections=x.sections, locations=x.locations, outro=outro)

    def load_interview(self, infile, number):
        SEGDIV = '====='
        MINIDIV = '==='
        NAMEDIV = '__'
        if not os.path.exists(infile):
            return
        with open(infile) as f:
            cont = f.read()
            clean_up = lambda x: x.replace('--', '&mdash;').split('\n')
            if type(cont) is str:
                lines = clean_up(cont)
            else:
                lines = clean_up(unidecode(cont))
            lines = [x.strip() for x in lines if x.strip()]
        if not lines:
            print 'ERROR: Could not read {0}'.format(infile)
            return
        seg = 1

        subject = ''
        intro = []
        sections = []
        locations = []

        cur_section_name = ''
        cur_section_lines = []
        for line in lines:
            if line == SEGDIV:
                seg += 1
                if seg > 5:
                    print 'ERROR: Too many SEGDIVs: {0}'.format(SEGDIV)
                    return
                if seg == 4 and cur_section_name:
                    if not cur_section_lines:
                        print 'ERROR: Empty section: {0}'.format(cur_section_name)
                        return
                    cur_section = Section(cur_section_name, cur_section_lines)
                    sections.append(cur_section)
                continue
            if seg == 1: # subject
                if subject:
                    print 'ERROR: Second subject line: {0}'.format(line)
                    return
                subject = line
            elif seg == 2: # intro
                intro.append(line)
            elif seg == 3: # interview
                if line.startswith(MINIDIV):
                    if cur_section_name:
                        if not cur_section_lines:
                            print 'ERROR: Empty section: {0}'.format(cur_section_name)
                            return
                        cur_section = Section(cur_section_name, cur_section_lines)
                        sections.append(cur_section)
                    if line.count(MINIDIV) != 2:
                        print 'ERROR: section name must be surrounded by MINIDIV {0}: {1}'.format(MINIDIV, line)
                        return
                    cur_section_name = line.split(MINIDIV)[1]
                    cur_section_lines = []
                elif line.startswith(NAMEDIV):
                    if not cur_section_name:
                        print 'ERROR: found line not in section: {0}'.format(line)
                        return
                    x = line.split(NAMEDIV)
                    if len(x) < 2:
                        print 'ERROR: NAMEDIV {0} must be mentioned twice in: {1}'.format(NAMEDIV, line)
                        return
                    name = x[1]
                    statement = NAMEDIV.join(x[2:]).strip()
                    cur_section_lines.append((name, statement))
                else:
                    if not cur_section_name:
                        print 'ERROR: found line not in section: {0}'.format(line)
                        return
                    cur_section_lines.append(('', line))
            elif seg == 4: # locations
                if line.count(MINIDIV) != 2:
                    print 'ERROR: Location line without two {0}: {1}'.format(MINIDIV, line)
                    return
                loc = [x.strip() for x in line.split(MINIDIV)]
                if loc[0] != str(len(locations)+1):
                    print 'ERROR: Location index not in sequence: {0}'.format(line)
                    return
                loc = Location(loc[1], loc[2])
                locations.append(loc)
        return Interview(number, subject, intro, sections, locations)

def main(settings, full_icon_url):
    media_dir = settings['media_dir']
    media_path = settings['abs_media_dir']
    if not os.path.exists(media_path):
        os.mkdir(media_path)
    return Root(media_dir, media_path, full_icon_url)

if __name__ == '__main__':
    main()
