import functools
import os
import re
import sys
from multiprocessing import Pipe, get_context

from impersonation import utils


class _run_as:
    """Context manager to run routines as given user."""

    def __init__(self, username):
        self.username = username

    def __enter__(self):
        os.setuid(utils.user_uid(self.username))
        os.setgid(utils.user_gid(self.username))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


def _target(conn, fn, username, *args, **kwargs):
    # run routine under given username
    try:
        with _run_as(username):
            ret = fn.__wrapped__(*args, **kwargs)
    except Exception as ex:
        ret = None
        err = ex
    else:
        err = None

    # pipe out the process result
    conn.send((ret, err))
    conn.close()


def impersonate(arg=None, username=None):
    ctx = get_context("spawn")
    p_conn, c_conn = Pipe()

    def decorator(fn):

        # apply decorator to each method
        if isinstance(fn, type):
            for name, attr in fn.__dict__.items():
                if callable(attr) and not re.match(r"__\w*__", name):
                    setattr(fn, name, decorator(attr))
            return fn

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # call wrapped function if no user impersonation
            if not username or username == utils.system_username():
                return fn(*args, **kwargs)

            cls_name = fn.__qualname__.split('.')[0]
            cls = vars(sys.modules[fn.__module__])[cls_name]
            func = getattr(cls, fn.__name__)
            target_args = (c_conn, func, username, *args)

            p = ctx.Process(target=_target, args=target_args, kwargs=kwargs)
            p.start()
            ret, err = p_conn.recv()
            if err:
                raise err
            p.join()
            return ret

        return wrapper

    if callable(arg):
        if isinstance(arg, type):
            decorator(arg)
            return arg
        else:
            return decorator(arg)
    return decorator
