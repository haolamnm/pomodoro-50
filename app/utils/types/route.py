from typing import Literal
from flask import Response
from werkzeug.wrappers import Response as Redirect


type StatusCode = Literal[200, 301, 302, 400, 401, 404, 500]

# general response with status code
type GenericResponse = tuple[Response, StatusCode]

# redirect response with status code
type RedirectResponse = tuple[Redirect, StatusCode]

# render_template response with status code
type RenderResponse = tuple[str, StatusCode]
