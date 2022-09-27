import functools
import os
import re
import sys
from multiprocessing import Pipe, get_context

from impersonation import utils


class _run_as:
    """Context manager to run routines as given user."""

    def __init__(self, uid, gid):
        self.uid = uid
        self.gid = gid

    def __enter__(self):
        os.setuid(self.uid)
        os.setgid(self.gid)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


def _target(conn, fn, ids, *args, **kwargs):
    # run routine under given username
    try:
        with _run_as(*ids):
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

            cls_name = fn.__qualname__.split(".")[0]
            cls = vars(sys.modules[fn.__module__])[cls_name]
            func = getattr(cls, fn.__name__)

            uid, gid = utils.pw_pair(username=username)
            target_args = (c_conn, func, (uid, gid), *args)
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
