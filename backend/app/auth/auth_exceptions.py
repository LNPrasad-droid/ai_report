class AuthError(Exception):
    pass


class FirebaseInitializationError(AuthError):
    pass


class TokenVerificationError(AuthError):
    pass


class UnauthorizedError(AuthError):
    pass


class RoleMismatchError(AuthError):
    pass
