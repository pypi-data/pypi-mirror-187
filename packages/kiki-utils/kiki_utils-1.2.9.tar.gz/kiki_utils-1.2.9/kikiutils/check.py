import os
import re


ALLOWED_EMAILS = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'aol.com',
    'hotmail.co.uk',
    'hotmail.fr',
    'msn.com',
    'wanadoo.fr',
    'live.com',
    'hotmail.it',
    'qq.com'
]

domain_pattern = re.compile(
    r'^(?:[a-zA-Z0-9]'  # First character of the domain
    r'(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)'  # Sub domain + hostname
    r'+[A-Za-z0-9][A-Za-z0-9-_]{0,61}'  # First 61 characters of the gTLD
    r'[A-Za-z]$'  # Last character of the gTLD
)


# Check

def isbytes(*args):
    """Determine whether it is bytes."""

    return all([isinstance(arg, bytes) for arg in args])


def isdomain(domain: str):
    """Check domain."""

    return domain_pattern.match(domain) is not None


def isemail(email: str):
    """Check email format and ping the domain."""

    if re.match(r'.*[+\-*/\\;&|\s​].*', email):
        return False

    domain = email.split('@')[-1].lower()
    return domain in ALLOWED_EMAILS or isdomain(domain)


def isdict(*args):
    """Determine whether it is dict."""

    return all([isinstance(arg, dict) for arg in args])


def isdir(*args):
    """Determine whether path is dir."""

    return all([os.path.isdir(arg) for arg in args])


def isfile(*args):
    """Determine whether path is file."""

    return all([os.path.isfile(arg) for arg in args])


def isint(*args):
    """Determine whether it is int."""

    return all([isinstance(arg, int) for arg in args])


def islist(*args):
    """Determine whether it is list."""

    return all([isinstance(arg, list) for arg in args])


def isstr(*args):
    """Determine whether it is str."""

    return all([isinstance(arg, str) for arg in args])
