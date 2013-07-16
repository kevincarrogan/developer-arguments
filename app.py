import functools
import random

import os
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from pystache.loader import Loader
from pystache import render

from flask import Flask


app = Flask(__name__)
app.debug = True
loader = Loader()


arguments = [
    (
        'CBV', 'FBV',
        ('django', 'python',)
    ),
    (
        'Linux', 'Mac OS X',
        ('os',)
    ),
    (
        'Emacs', 'Vi',
        ('editors',)
    ),
    (
        'Semi-colons', 'No semi-colons',
        ('javascript',)
    ),
    (
        'Mac', 'PC',
        ('os',)
    ),
]


def render_template(section_name):
    template = loader.load_name('templates/%s' % section_name)

    def func_wrapper(func):
        @functools.wraps(func)
        def renderer():
            context = func()

            return render(
                template,
                context,
            )
        return renderer

    return func_wrapper


@app.route('/')
@render_template('home')
def home():
    argument = random.choice(arguments)

    challenger_one = argument[0]
    challenger_two = argument[1]
    tags = argument[2]

    return {
        'challenger_one': challenger_one,
        'challenger_two': challenger_two,
        'tags': tags,
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
