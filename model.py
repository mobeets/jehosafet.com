import csv
import os.path
from unidecode import unidecode
from markdown import markdown

from mako.lookup import TemplateLookup

FILETYPES = ['.pdf', '.jpg', '.png', '.gif', '.txt', '.html', '.md']
ROOT_URL = 'http://www.jehosafet.com/'

serve_pdf = lambda url: '<iframe src="http://docs.google.com/gview?url=' + ROOT_URL + url + '&embedded=true" style="width:718px; height:700px;" frameborder="0"></iframe>'
serve_img = lambda url: '<img src="{0}" style="max-width:100%;">'.format(url)
wrap_in_gray_div = lambda text: '<div style="padding:10px; background-color:#E4E4E4;"><br>' + text + '<br></div>'
def serve_raw(url):
    if url.startswith('/'):
        url = url[1:]
    replace_newline_with_br = lambda text: text.replace('\n', '<br>')
    try:
        with open(url) as f:
            return wrap_in_gray_div(replace_newline_with_br(unidecode(f.read())))
    except Exception, e:
        print str(e)
        return wrap_in_gray_div('PLACEHOLDER')

def serve_html(filename):
    lookup = TemplateLookup(directories=['templates'])
    tmp = lookup.get_template(filename)
    return tmp.render()

def serve_markdown(filedir, filename):
    localdir = filedir
    if localdir.startswith('/'):
        localdir = filedir[1:]
    path = os.path.join(localdir, filename)
    out = unidecode(open(path).read())
    out = markdown(out, ['extra'])
    out = out.replace('--', '&mdash;')
    return out

def load_content(media_dir, key, filetype):
    filename = key + filetype
    path = '/' + '/'.join([media_dir, filename])
    if filetype == '.pdf':
        return serve_pdf(path)
    elif filetype in ['.jpg', '.jpeg', '.gif', '.png']:
        return serve_img(path)
    elif filetype == '.txt':
        return serve_raw(path)
    elif filetype == '.md':
        return serve_markdown(media_dir, filename)
    elif filetype == '.html':
        return serve_html(filename)
    return 'CONTENT PLACEHOLDER'

def load(infile):
    with open(infile, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        items = []
        for row in csvreader:
            item = row
            if item['date'].startswith('#'):
                continue
            if item['url'].startswith('.'):
                if item['url'] not in FILETYPES:
                    raise Exception("ILLEGAL KIND: {0}.{1}".format(item['key'], item['url']))
                item['kind'] = item['url']
                item['url'] = 'item/{0}'.format(item['key'])
            else:
                item['url'] = item['url']
                item['kind'] = None
            items.append(item)
        return items
