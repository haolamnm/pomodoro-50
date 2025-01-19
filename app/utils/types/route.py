from typing import Literal
from flask import Response
from werkzeug.wrappers import Response as Redirect


# Corrected type alias for status codes
type StatusCode = Literal[200, 301, 404, 500]

# General response with status code
type GenericResponse = tuple[Response, StatusCode]

# Redirect response with status code
type RedirectResponse = tuple[Redirect, StatusCode]
