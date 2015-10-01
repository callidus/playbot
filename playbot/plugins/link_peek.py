

from __future__ import absolute_import

import re
from six.moves.urllib import request

def peek(bot, c, e):
    msg = e.arguments[0].strip()
    msg = re.search("(http[^ ]*)", msg)
    if msg is None:
        return
    url = msg.group(1)
    req = request.Request(url)
    response = request.urlopen(req)
    the_page = response.read().decode('windows-1252')
    title = re.search("<title>([^<]*)</title>", str(the_page)).group(1)
    return "Link peek: %s" % title
