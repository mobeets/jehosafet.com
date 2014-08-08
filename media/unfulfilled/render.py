import os.path
from collections import namedtuple
from unidecode import unidecode
from mako.lookup import TemplateLookup

CURDIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
TMPDIR = os.path.abspath(os.path.join(CURDIR, '..', '..', 'templates'))
MEDIA_DIR = 'media/unfulfilled'
OUTRO_FILE = 'end_graph.txt'

Section = namedtuple('Section', 'name statements')
Location = namedtuple('Location', 'dt name')
Interview = namedtuple('Interview', 'title photo number subject intro sections locations')

issue_filename = lambda number: 'unfulfilled-{0}.interview'.format(number)
html_filename = lambda number: 'unfulfilled-{0}.html'.format(number)
make_title = lambda number: 'Unfulfilled #{0}'.format(number)
photo_path = lambda number: 'unfulfilled-{0}.png'.format(number)

def make_photo(number, media_path):
    path = photo_path(number)
    if not os.path.exists(os.path.join(media_path, path)):
        return 'ERROR: Could not find image file: {0}'.format(os.path.join(media_path, path))
    return path

def load_interview(number, media_path):
    infile = os.path.join(media_path, issue_filename(number))
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
    return Interview(make_title(number), make_photo(number, media_path), number, subject, intro, sections, locations)

def load_issues(media_path):
    ds = []
    still_got_it = True
    i = 1
    while still_got_it:
        issue = load_interview(i, media_path)
        if issue:
            ds.append(issue)
        else:
            still_got_it = False
        i += 1
    return ds

def write(media_path, content, i):
    infile = os.path.join(media_path, html_filename(i))
    with open(infile, 'w') as f:
        f.write(content)

def main(output_dir=TMPDIR, media_dir=MEDIA_DIR, abs_media_dir=CURDIR):
    """
    all files should be accessible in abs_media_dir
    media_dir is for html access
    output_dir is where html is written
    """
    outro = open(os.path.join(abs_media_dir, OUTRO_FILE)).read()
    tmp = TemplateLookup(directories=[abs_media_dir]).get_template('interview.html')
    for i, issue in enumerate(load_issues(abs_media_dir)):
        content = tmp.render(title=issue.title, mediadir=media_dir, photo=issue.photo, subject=issue.subject, intro=issue.intro, sections=issue.sections, locations=issue.locations, outro=outro)
        write(output_dir, content, i+1)

if __name__ == '__main__':    
    main()
