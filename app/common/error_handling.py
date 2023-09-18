class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass


class Unauthorized(AppErrorBaseClass):
    pass


class Conflict(AppErrorBaseClass):
    pass