from __future__ import absolute_import

import sys

from . import ssl_match_hostname

# Downstream redistributors which have debundled our dependencies should also
# patch this value to be true. This will trigger the additional patching
# to cause things like "six" to be available as pip.
DEBUNDLED = True
 
 # Define a small helper function to alias our vendored modules to the real ones
# if the vendored ones do not exist. This idea of this was taken from
# https://github.com/kennethreitz/requests/pull/2567.
def vendored(modulename):
    vendored_name = "{0}.{1}".format(__name__, modulename)

    try:
        __import__(vendored_name, globals(), locals(), level=0)
    except ImportError:
        __import__(modulename, globals(), locals(), level=0)
        sys.modules[vendored_name] = sys.modules[modulename]
        base, head = vendored_name.rsplit(".", 1)
        setattr(sys.modules[base], head, sys.modules[modulename])


# If we're operating in a debundled setup, then we want to go ahead and trigger
# the aliasing of our vendored libraries as well as looking for wheels to add
# to our sys.path. This will cause all of this code to be a no-op typically
# however downstream redistributors can enable it in a consistent way across
# all platforms.
if DEBUNDLED:
    # Actually alias all of our vendored dependencies.
    vendored("six")
    vendored("six.moves")
    vendored("six.moves.http_client")
    vendored("six.moves.queue")
    vendored("six.moves.urllib")
    vendored("six.moves.urllib.parse")

__all__ = ('ssl_match_hostname', 'six')
