import os
import pwd


def pw_pair(username):
    pwnam = pwd.getpwnam(username)
    return pwnam.pw_uid, pwnam.pw_gid


def system_username():
    return pwd.getpwuid(os.getuid()).pw_name
