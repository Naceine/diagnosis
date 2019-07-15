
from api.app import app

__all__ = ['router']


class Router:
    # noinspection PyUnresolvedReferences,PyUnusedFunction
    """A Wrapper decorator around `Flask.app.route`. Enables route specialization.

    Methods:
        @staticmethod
        route(rule, name=None, **options)
            # Use name to generate a dynamic URL structure `/<name>/<rule>`.

        @staticmethod
        api(rule, **options)
            # calls Router.route with default name="api" -> `/api/*`.

    Examples:
        ```python
        >>> # Home page router.
        >>> router.route('/', methods=['GET'])
        ... def index():
        ...   return "<h1>Hello, World!</h1>"
        >>>
        >>> # Creating dummy (simple) user edit API.
        >>> def edit_user(uid=None):
        ...   print('Updating user with id', uid)
        ...   return True
        >>>
        >>> # Router endpoint.
        >>> router.api('/users/<uid:int>/edit', methods=['POST'])
        ... def edit(uid=None):
        ...   status = edit_user(uid)
        ...   return jsonify({
        ...     'status': status,
        ...     'message': 'Updated successfully!'
        ...   })
        >>>
        ```
    """

    @staticmethod
    def route(rule, name=None, **options):
        rule = ('/{}/{}'.format(name.strip('/'),
                                rule.lstrip('/'))
                if name else rule)

        def decorator(f):
            # Decorate the Flask's app.route
            d = app.route(rule, **options)
            return d(f)

        return decorator

    @staticmethod
    def api(rule, **options):
        return Router.route(rule, name='api', **options)


# Create a public alias for Router.
router = Router
