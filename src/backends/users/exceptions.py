from src.backends.exceptions import GeneralException


class UserNotFoundException(GeneralException):
    pass

class DuplicateUserException(GeneralException):
    pass