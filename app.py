import functools
import random
import itertools

import os
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from pystache.loader import Loader
from pystache import render

from flask import Flask, abort, url_for


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
    (
        ('jQuery animations', 'CSS Animations'),
        ('web'),
    ),
    (
        ('Boolean', 'boolean',),
        (),
    ),
    (
        ('DHH', 'TDD',),
        ('Testing', 'Internet "celebrities"'),
    ),
    (
        ('Swift', 'Objective C'),
        ('Languages', 'iOS',),
    ),
    (
        ('Grunt', 'Gulp'),
        ('Build tools',),
    ),
    (
        ('Flask', 'Bottle'),
        ('Frameworks',),
    ),
    (
        ('MIT', 'GPL'),
        ('Licenses',),
    ),
    (
        ('Inverted', 'Non-inverted mouse'),
        ('Gaming',),
    ),
    (
        ('Marvel', 'DC'),
        ('Comics',),
    ),
    (
        ('Star Wars', 'Star Trek'),
        (),
    ),
    (
        ('ORMs', 'Raw SQL'),
        (),
    ),
]


def slugify(string):
    return string.lower().replace(' ', '-')


routes = {}

for argument in arguments:
    challengers, tags = argument

    for perm in itertools.permutations(challengers):
        slugs = tuple(slugify(c) for c in perm)

        routes[slugs] = (perm, tags,)


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


def get_context_data(challenger_one, challenger_two):
    permalink = url_for(
        'permalink',
        challenger_one=slugify(challenger_one),
        challenger_two=slugify(challenger_two),
    )

    return {
        'challenger_one': challenger_one,
        'challenger_two': challenger_two,
        'permalink': permalink,
    }


@app.route('/<challenger_one>-vs-<challenger_two>/')
@render_template('home')
def permalink(challenger_one, challenger_two):
    try:
        challengers, _ = routes[(challenger_one, challenger_two,)]
    except KeyError:
        abort(404)
    else:
        return get_context_data(*challengers)


@app.route('/')
@render_template('home')
def home():
    argument = random.choice(arguments)

    challengers, _ = argument
    random.shuffle(list(challengers))

    return get_context_data(*challengers)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
