import inspect

from aiohttp import web
from http import HTTPStatus
from functools import wraps
from typing import Any, Optional
from aiohttp import web
from aiohttp_session import get_session, Session

# from app.lib.auth import get_auth_user, select_user_by_id
# from app.lib.enums import EnumCodes
# from app.lib.helpers import make_api_error


def build_next_url_key(role: int) -> str:
    """Build key for storing next URL in session due to user role."""
    return 'next_key_{0}'.format(role)


def build_url(request: web.Request,
              route_name: str,
              *,
              absolute: bool=True,
              get: dict=None,
              **context) -> str:
    """Build absolute or relative URL for given route name."""
    path = request.app.router[route_name].url_for(**context).with_query(get)
    if not absolute:
        return str(path)
    return '{0.scheme}://{0.host}{1}'.format(request, path)


def get_handler_request(mixed: Any) -> web.Request:
    """Return request for view handler function or method.
    For view function request is a first arg. For class method get it as
    ``self.request``.
    """
    return mixed.request if hasattr(mixed, 'request') else mixed


# def login_required(handler_func=None,
#                    *,
#                    role=EnumCodes.role_user.value,
#                    redirect_to_login=False):
#     """Show not authenticated error if user is not logged in.
#     When role is supplied, check that logged in user has that role. When
#     redirect to login is supplied, redirect user to login page, do not show
#     the error.
#     """
#     def decorator(handler):
#         @wraps(handler)
#         async def wrapper(mixed, *args, **kwargs):
#             request = get_handler_request(mixed)
#             session = await get_session(request)
#             # Exit as early as possible, no user in session - no need to open
#             # database connection
#             user_id = session.get('user')
#             not_logged_in_args = (request, session, role, redirect_to_login)
#             if not user_id:
#                 return not_logged_in(*not_logged_in_args)
#             # Check that user in session is valid and have necessary role
#             async with request.app['db'].acquire() as conn:
#                 user = await select_user_by_id(conn, user_id)
#                 if not (user and user.role_id >= role):
#                     return not_logged_in(*not_logged_in_args)
#                 # Redirect user to originally requested URL
#                 redirect = redirect_to_next_url(request, session, role)
#                 if redirect:
#                     return redirect
#                 # Pass user to handler function
#                 if 'user' in inspect.getfullargspec(handler).args:
#                     kwargs['user'] = user
#                 return await handler(mixed, *args, **kwargs)
#         return wrapper
#     return decorator(handler_func) if callable(handler_func) else decorator


# def not_logged_in(request: web.Request,
#                   session: Session,
#                   role: int,
#                   redirect_to_login: bool) -> web.Response:
#     """Process case, when there is no logged in user in session."""
#     # Remember originally requested URL
#     store_next_url(request, session, role)
#     # Redirect user to login page
#     if redirect_to_login:
#         return redirect(request, 'login')
#     # Make API error in other cases
#     return make_api_error(
#         status=403,
#         code=EnumCodes.login_required.value)


def redirect(request: web.Request,
             route_name: str,
             *,
             get: dict=None,
             **context) -> web.Response:
    """Helper function to redirect to given route."""
    return web.HTTPFound(build_url(
        request,
        route_name,
        absolute=False,
        get=get,
        **context))


# def redirect_to_app(handler):
#     """Decorator to redirect to app if user is logged in."""
#     @wraps(handler)
#     async def wrapper(mixed, *args, **kwargs):
#         request = get_handler_request(mixed)
#         async with request.app['db'].acquire() as conn:
#             user = await get_auth_user(request, conn)
#         if user:
#             return redirect(request, 'app', tail='')
#         return await handler(mixed, *args, **kwargs)
#     return wrapper


def redirect_to_next_url(request: web.Request,
                         session: Session,
                         role: int) -> Optional[web.Response]:
    """Redirect to originally request URL if session contains it.
    Before redirect remove that URL from session, so user will not be
    redirected again on next request.
    """
    key = build_next_url_key(role)
    url = session.get(key)
    if url:
        del session[key]
        return web.HTTPFound(url)


def store_next_url(request: web.Request, session: Session, role: int) -> None:
    """Store next URL to session.
    This allow to redirect user back to originally requested page. The key
    stored to session due to role of page required, which means logged in
    regular user will not be redirected to next admin page if he somehow
    request it.
    """
    request_url = request.url.relative().human_repr()
    # Ignore requesting API, download or print URLs
    if (
        request_url[:5] == '/api/' or
        request_url[:10] == '/download/' or
        request_url[:7] == '/print/'
    ):
        return
    session[build_next_url_key(role)] = request_url


# Make shortcuts for ``login_required`` decorators
# admin_required = login_required(role=EnumCodes.role_admin.value)
# redirect_to_login = login_required(redirect_to_login=True)


def http404():
    return web.json_response(
        data={'error': 'Not found'},
        status=HTTPStatus.NOT_FOUND
    )


def http400():
    return web.json_response(
        data={'error': 'Invalid request'},
        status=HTTPStatus.BAD_REQUEST
    )


def http500():
    return web.json_response(
        data={'error': 'Server got itself in trouble'},
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )
