from typing import TypedDict, Literal
from flask import Response


class RouteData(TypedDict):
	message: str
	category: Literal['success', 'info', 'warning', 'danger']
	redirect: str


type StausCode = Literal[200, 301, 400, 401, 403, 404, 500]


type RouteResponse = tuple[Response, StausCode]
