from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(cookies):
    print("================")
    print(cookies)
    if 'usertoken' not in cookies:
        return AnonymousUser()
    try:
        usertoken = cookies['usertoken']
        print(usertoken)
        return Token.objects.get(key=usertoken).user
    except Exception:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """
    Inner class that is instantiated once per scope.
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        if settings.DEBUG:
            print(self.scope)
        if 'usertoken' in self.scope["cookies"]:
            self.scope['user'] = await get_user(self.scope["cookies"])
        else:
            query_string = self.scope["query_string"].decode('utf-8')
            self.scope['user'] = await get_user({'usertoken':query_string})

        # Instantiate our inner application
        inner = self.inner(self.scope)

        return await inner(receive, send)


TokenMiddlewareStack = lambda inner: CookieMiddleware(
    SessionMiddleware (TokenAuthMiddleware(inner))
)