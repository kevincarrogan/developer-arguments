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
    (
        ('CBV', 'FBV',),
        ('django', 'python',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=098146730X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1430258098&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Linux', 'Mac OS X',),
        ('os',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449316697&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=059652062X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Emacs', 'Vim',),
        ('editors',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0596006489&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=059652983X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Semi-colons', 'No semi-colons',),
        ('javascript',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0596517742&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0596805527&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Mac', 'PC',),
        ('os',),
        (),
    ),
    (
        ('Consoles', 'PC',),
        ('games',),
        (),
    ),
    (
        ('Angular', 'Backbone',),
        ('javascript',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449344852&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449328253&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Ruby on Rails', 'Django',),
        ('frameworks',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1937785564&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1430258098&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('PHP', 'Anything else',),
        ('languages',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449392776&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=144936375X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Feature switching', 'Branching',),
        ('workflow',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449325866&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1430218339&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Meetings', 'Doing actual work',),
        ('workflow',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0740777351&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0321579364&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('IDE', 'Text Editor',),
        ('editors',),
        (),
    ),
    (
        ('iOS', 'Android',),
        ('os',),
        (),
    ),
    (
        ('XBox', 'PlayStation',),
        ('games',),
        (),
    ),
    (
        ('Compiled', 'Interpreted',),
        ('languages',),
        (),
    ),
    (
        ('Spaces', 'Tabs',),
        ('code',),
        (),
    ),
    (
        ('Photoshop', 'Gimp',),
        ('editors',),
        (),
    ),
    (
        ('CLI', 'GUI',),
        (),
        (),
    ),
    (
        ('XML', 'JSON',),
        ('formats',),
        (),
    ),
    (
        ('CoffeeScript', 'Plain JS',),
        ('languages',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449321054&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0596517742&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('NoSQL', 'SQL',),
        ('databases',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0321826620&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1934356921&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('MySQL', 'Postgres',),
        ('databases',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=059652708X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449326331&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        )
    ),
    (
        ('Pronounced OS eks', 'Pronounced OS ten',),
        ('naming',),
        (),
    ),
    (
        ('Pronounced gif', 'Pronounced gif',),
        ('naming',),
        (),
    ),
    (
        ('Top posting', 'Bottom posting',),
        ('email',),
        (),
    ),
    (
        ('SysV', 'BSD',),
        ('os',),
        (),
    ),
    (
        ('Sun OS', 'Solaris',),
        ('os',),
        (),
    ),
    (
        ('Carbon', 'Cocoa',),
        ('frameworks',),
        (),
    ),
    (
        ('Sockets', 'Streams',),
        (),
        (),
    ),
    (
        ('IPv4', 'IPv6',),
        ('protocols',),
        (),
    ),
    (
        ('REST', 'SOAP',),
        ('protocols',),
        (),
    ),
    (
        ('ASCII', 'EBCDIC',),
        (),
        (),
    ),
    (
        ('Little endian', 'Big endian',),
        ('fundamentals'),
        (),
    ),
    (
        ('PowerPC', 'Intel',),
        ('hardware',),
        (),
    ),
    (
        ('nVidia', 'ATI',),
        ('hardware',),
        (),
    ),
    (
        ('OpenGL', 'DirectX',),
        ('frameworks',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=159863528X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1435458958&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Git', 'Mercurial',),
        ('versioning',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449325866&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0596800673&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('Native', 'Web',),
        (),
        (),
    ),
    (
        ('BSD KNF Style', 'Allman Style',),
        ('code',),
        (),
    ),
    (
        ('FP', 'OOP',),
        ('languages',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449365515&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=B00BP83RMO&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        )
    ), 
    (
        ('Java', 'C++',),
        ('languages',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449319246&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0131103628&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        )
    ),
    (
        ('Python', 'Ruby',),
        ('languages',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449355730&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=0596516177&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        )
    ),
    (
        ('Zsh', 'Bash',),
        ('os',),
        (),
    ),
    (
        ('LESS', 'SASS',),
        ('CSS extensions',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=178216376X&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=B00BKXQTBA&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        ),
    ),
    (
        ('jQuery animations', 'CSS Animations'),
        ('web'),
        (),
    ),
    (
        ('Boolean', 'boolean',),
        (),
        (),
    ),
    (
        ('DHH', 'TDD',),
        ('Testing', 'Internet "celebrities"'),
        (),
    ),
    (
        ('Swift', 'Objective C'),
        ('Languages', 'iOS',),
        (),
    ),
    (
        ('Grunt', 'Gulp'),
        ('Build tools',),
        (),
    ),
    (
        ('Flask', 'Bottle'),
        ('Frameworks',),
        (
            '<iframe src="http://rcm-eu.amazon-adsystem.com/e/cm?t=develoargume-21&o=2&p=8&l=as1&asins=1449372627&ref=tf_til&fc1=000000&IS2=1&lt1=_blank&m=amazon&lc1=0000FF&bc1=FFFFFF&bg1=FFFFFF&f=ifr" style="width:120px;height:240px;" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>',
        )
    ),
    (
        ('MIT', 'GPL'),
        ('Licenses',),
        (),
    ),
    (
        ('Inverted', 'Non-inverted mouse'),
        ('Gaming',),
        (),
    ),
    (
        ('Marvel', 'DC'),
        ('Comics',),
        (),
    ),
    (
        ('Star Wars', 'Star Trek'),
        (),
        (),
    ),
    (
        ('ORMs', 'Raw SQL'),
        (),
        (),
    ),
]


def slugify(string):
    return string.lower().replace(' ', '-')


routes = {}

for argument in arguments:
    challengers, tags, affiliate_links = argument

    for perm in itertools.permutations(challengers):
        slugs = tuple(slugify(c) for c in perm)

        routes[slugs] = (perm, tags, affiliate_links)


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


def get_context_data(challenger_one, challenger_two, tags, affiliate_links, perm=False):
    permalink = url_for(
        'permalink',
        challenger_one=slugify(challenger_one),
        challenger_two=slugify(challenger_two),
    )

    return {
        'challenger_one': challenger_one,
        'challenger_two': challenger_two,
        'permalink': permalink,
        'tags': tags,
        'affiliate_links': affiliate_links,
        'perm': perm,
    }


@app.route('/<challenger_one>-vs-<challenger_two>/')
@render_template('home')
def permalink(challenger_one, challenger_two):
    try:
        challengers, tags, affiliate_links = routes[(challenger_one, challenger_two,)]
    except KeyError:
        abort(404)
    else:
        challenger_one, challenger_two = challengers
        return get_context_data(
            challenger_one,
            challenger_two,
            tags,
            affiliate_links,
            perm=True,
        )


@app.route('/')
@render_template('home')
def home():
    argument = random.choice(arguments)

    challengers, tags, affiliate_links = argument
    challengers = list(challengers)
    random.shuffle(challengers)

    challenger_one, challenger_two = challengers

    return get_context_data(
        challenger_one,
        challenger_two,
        tags,
        affiliate_links,
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
