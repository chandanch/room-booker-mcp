class AuthenticationError(Exception):
    """The caller could not be authenticated."""


class AuthorizationError(Exception):
    """The authenticated caller is not authorized."""
