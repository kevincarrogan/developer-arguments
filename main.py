import itertools
import random

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from arguments import arguments

templates = Jinja2Templates(directory="templates")


def slugify(string):
    return string.lower().replace(" ", "-")


def get_context_data(request, challenger_one, challenger_two, perm=False):
    permalink = request.url_for(
        "permalink",
        challenger_one=slugify(challenger_one),
        challenger_two=slugify(challenger_two),
    )

    return {
        "challenger_one": challenger_one,
        "challenger_two": challenger_two,
        "permalink": permalink,
        "perm": perm,
        "request": request,
    }


valid_routes = {}

for challengers in arguments:
    for perm in itertools.permutations(challengers):
        slugs = tuple(slugify(c) for c in perm)

        valid_routes[slugs] = perm


def permalink(challenger_one, challenger_two):
    try:
        challengers = routes[(challenger_one, challenger_two)]
    except KeyError:
        return Response("Not found", status_code=404)
    else:
        challenger_one, challenger_two = challengers

        return templates.TemplateResponse(
            "argument.html", get_context_data(challenger_one, challenger_two, perm=True)
        )


def home(request):
    challengers = random.choice(arguments)
    challengers = list(challengers)
    random.shuffle(challengers)

    challenger_one, challenger_two = challengers

    return templates.TemplateResponse(
        "argument.html", get_context_data(request, challenger_one, challenger_two)
    )


routes = [
    Route("/", home),
    Route("/{challenger_one}-vs-{challenger_two}/", permalink),
    Mount("/static", StaticFiles(directory="static")),
]

app = Starlette(routes=routes)
