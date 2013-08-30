import functools
import random

import os
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from pystache.loader import Loader
from pystache import render

from flask import Flask, redirect, abort


app = Flask(__name__)
app.debug = True
loader = Loader()


arguments = [
    (
        ('CBV', 'FBV',),
        ('django', 'python',)
    ),
    (
        ('Linux', 'Mac OS X',),
        ('os',)
    ),
    (
        ('Emacs', 'Vim',),
        ('editors',)
    ),
    (
        ('Semi-colons', 'No semi-colons',),
        ('javascript',)
    ),
    (
        ('Mac', 'PC',),
        ('os',)
    ),
    (
        ('Consoles', 'PC',),
        ('games',)
    ),
    (
        ('Angular', 'Backbone',),
        ('javascript',)
    ),
    (
        ('Ruby on Rails', 'Django',),
        ('frameworks',)
    ),
    (
        ('PHP', 'Anything else',),
        ('languages',)
    ),
    (
        ('Feature switching', 'Branching',),
        ('workflow',)
    ),
    (
        ('Meetings', 'Doing actual work',),
        ('workflow',)
    ),
    (
        ('IDE', 'Text Editor',),
        ('editors',),
    ),
    (
        ('iOS', 'Android',),
        ('os',),
    ),
    (
        ('XBox', 'PlayStation',),
        ('games',),
    ),
    (
        ('Compiled', 'Interpreted',),
        ('languages',),
    ),
    (
        ('Spaces', 'Tabs',),
        ('code',),
    ),
    (
        ('Photoshop', 'Gimp',),
        ('editors',),
    ),
    (
        ('CLI', 'GUI',),
        (),
    ),
    (
        ('XML', 'JSON',),
        ('formats',),
    ),
    (
        ('CoffeeScript', 'Plain JS',),
        ('languages',),
    ),
    (
        ('NoSQL', 'SQL',),
        ('databases',),
    ),
    (
        ('MySQL', 'Postgres',),
        ('databases',),
    ),
    (
        ('Pronounced OS eks', 'Pronounced OS ten',),
        ('naming',),
    ),
    (
        ('Pronounced gif', 'Pronounced gif',),
        ('naming',),
    ),
    (
        ('Top posting', 'Bottom posting',),
        ('email',),
    ),
    (
        ('SysV', 'BSD',),
        ('os',),
    ),
    (
        ('Sun OS', 'Solaris',),
        ('os',),
    ),
    (
        ('Carbon', 'Cocoa',),
        ('frameworks',),
    ),
    (
        ('Sockets', 'Streams',),
        (),
    ),
    (
        ('IPv4', 'IPv6',),
        ('protocols',),
    ),
    (
        ('REST', 'SOAP',),
        ('protocols',),
    ),
    (
        ('ASCII', 'EBCDIC',),
        (),
    ),
    (
        ('Little endian', 'Big endian',),
        ('fundamentals'),
    ),
    (
        ('PowerPC', 'Intel',),
        ('hardware',),
    ),
    (
        ('nVidia', 'ATI',),
        ('hardware',),
    ),
    (
        ('OpenGL', 'DirectX',),
        ('frameworks',),
    ),
    (
        ('Git', 'Mercurial',),
        ('versioning',),
    ),
    (
        ('Native', 'Web',),
        (),
    ),
    (
        ('BSD KNF Style', 'Allman Style',),
        ('code',),
    ),
    (
        ('FP', 'OOP',),
        ('languages',),
    ), 
    (
        ('Java', 'C++',),
        ('languages',),
    ),
    (
        ('Python', 'Ruby',),
        ('languages',),
    ),
    (
        ('Zsh', 'Bash',),
        ('os',),
    ),
    (
        ('LESS', 'SASS',),
        ('CSS extensions',),
    ),
]


def slugify(string):
    return string.lower().replace(' ', '-')


routes = {
    (slugify(argument[0][0]), slugify(argument[0][1]),): (argument[0][0], argument[0][1],) for argument in arguments
}


def render_template(section_name):
    template = loader.load_name('templates/%s' % section_name)

    def func_wrapper(func):

        @functools.wraps(func)
        def renderer(*args, **kwargs):
            context = func(*args, **kwargs)

            return render(
                template,
                context,
            )
        return renderer

    return func_wrapper


@app.route('/')
def home():
    challengers = random.choice(arguments)[0]
    challengers = map(slugify, challengers)

    challenger_one = challengers[0]
    challenger_two = challengers[1]

    return redirect('/%s-vs-%s/' % (challenger_one, challenger_two,))


@app.route('/<argument>/')
@render_template('argument')
def argument(argument):
    route_key = tuple(argument.split('-vs-'))

    try:
        challengers = routes[route_key]

        return {
            'challenger_one': challengers[0],
            'challenger_two': challengers[1],
        }
    except KeyError:
        return abort(404)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
