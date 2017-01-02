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

from flask_compress import Compress

from arguments import arguments


app = Flask(__name__)
Compress(app)

loader = Loader()

home_template = loader.load_name('templates/home')


def slugify(string):
    return string.lower().replace(' ', '-')


routes = {}

for challengers in arguments:
    for perm in itertools.permutations(challengers):
        slugs = tuple(slugify(c) for c in perm)

        routes[slugs] = perm


def render_template():
    def func_wrapper(func):
        @functools.wraps(func)
        def renderer(*args, **kwargs):
            context = func(*args, **kwargs)

            return render(
                home_template,
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
@render_template()
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
@render_template()
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
