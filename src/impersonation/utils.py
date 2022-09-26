import os
import pwd


def user_uid(username):
    return pwd.getpwnam(username).pw_uid


def user_gid(username):
    return pwd.getpwnam(username).pw_gid


def system_username():
    return pwd.getpwuid(os.getuid()).pw_name
