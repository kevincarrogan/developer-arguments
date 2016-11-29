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
loader = Loader()


arguments = [
    ('CBV', 'FBV',),
    ('Linux', 'Mac OS X',),
    ('Emacs', 'Vim',),
    ('Semi-colons', 'No semi-colons',),
    ('Mac', 'PC',),
    ('Consoles', 'PC',),
    ('Angular', 'Backbone',),
    ('Ruby on Rails', 'Django',),
    ('PHP', 'Anything else',),
    ('Feature switching', 'Branching',),
    ('Meetings', 'Doing actual work',),
    ('IDE', 'Text Editor',),
    ('iOS', 'Android',),
    ('XBox', 'PlayStation',),
    ('Compiled', 'Interpreted',),
    ('Spaces', 'Tabs',),
    ('Photoshop', 'Gimp',),
    ('CLI', 'GUI',),
    ('XML', 'JSON',),
    ('CoffeeScript', 'JavaScript',),
    ('NoSQL', 'SQL',),
    ('MySQL', 'Postgres',),
    ('Pronounced OS eks', 'Pronounced OS ten',),
    ('Pronounced gif', 'Pronounced gif',),
    ('Top posting', 'Bottom posting',),
    ('SysV', 'BSD',),
    ('Sun OS', 'Solaris',),
    ('Carbon', 'Cocoa',),
    ('Sockets', 'Streams',),
    ('IPv4', 'IPv6',),
    ('REST', 'SOAP',),
    ('ASCII', 'EBCDIC',),
    ('Little endian', 'Big endian',),
    ('PowerPC', 'Intel',),
    ('nVidia', 'ATI',),
    ('OpenGL', 'DirectX',),
    ('Git', 'Mercurial',),
    ('Native', 'Web',),
    ('BSD KNF Style', 'Allman Style',),
    ('FP', 'OOP',),
    ('Java', 'C++',),
    ('Python', 'Ruby',),
    ('Zsh', 'Bash',),
    ('LESS', 'SASS',),
    ('jQuery animations', 'CSS Animations'),
    ('Boolean', 'boolean',),
    ('DHH', 'TDD',),
    ('Swift', 'Objective C'),
    ('Grunt', 'Gulp'),
    ('Flask', 'Bottle'),
    ('MIT', 'GPL'),
    ('Inverted', 'Non-inverted mouse'),
    ('Marvel', 'DC'),
    ('Star Wars', 'Star Trek'),
    ('ORMs', 'Raw SQL'),
    ('Angular', 'React'),
    ('Batman', 'Superman'),
    ('Code', 'Sleep'),
    ('Morrowind', 'Skyrim'),
    ('Covariance', 'Contravariance'),
    ('Java', 'C#'),
    ('Zed Shaw', 'Python 3'),
    ('Python 2', 'Python 3'),
    ('Vue', 'React'),
    ('Replicant', 'Not a replicant'),
]


def slugify(string):
    return string.lower().replace(' ', '-')


routes = {}

for challengers in arguments:
    for perm in itertools.permutations(challengers):
        slugs = tuple(slugify(c) for c in perm)

        routes[slugs] = perm


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


def get_context_data(challenger_one, challenger_two, perm=False):
    permalink = url_for(
        'permalink',
        challenger_one=slugify(challenger_one),
        challenger_two=slugify(challenger_two),
    )

    return {
        'challenger_one': challenger_one,
        'challenger_two': challenger_two,
        'permalink': permalink,
        'perm': perm,
    }


@app.route('/<challenger_one>-vs-<challenger_two>/')
@render_template('home')
def permalink(challenger_one, challenger_two):
    try:
        challengers = routes[(challenger_one, challenger_two,)]
    except KeyError:
        abort(404)
    else:
        challenger_one, challenger_two = challengers
        return get_context_data(
            challenger_one,
            challenger_two,
            perm=True,
        )


@app.route('/')
@render_template('home')
def home():
    challengers = random.choice(arguments)
    challengers = list(challengers)
    random.shuffle(challengers)

    challenger_one, challenger_two = challengers

    return get_context_data(
        challenger_one,
        challenger_two,
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
