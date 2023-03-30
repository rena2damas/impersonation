import os


__all__ = (
    "pw_username",
    "pw_pair",
)


def pwd():
    try:
        import pwd

        return pwd
    except ImportError:
        raise OSError


def pw_username():
    return pwd().getpwuid(os.getuid()).pw_name


def pw_pair(username):
    pwnam = pwd().getpwnam(username)
    return pwnam.pw_uid, pwnam.pw_gid
