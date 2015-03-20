import re
import urllib.request
import urllib.parse

class PeekResponse: pass

def peek(bot, c, e):
    msg = e.arguments[0].strip()
    msg = re.search("(http[^ ]*)", msg)
    if msg is None:
        return
    msg = msg.group(1)
    peek = PeekResponse()
    try:
        peek.title = peekTitle(msg)
    except Exception:
        pass        
    return peek

def peekTitle(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    the_page = response.read().decode('windows-1252')
    title = re.search("<title>([^<]*)</title>",str(the_page)).group(1)
    return title

# Quick Test
def test_all():
    class TestMsg:
        def __init__(self):
            self.arguments = ["goto https://www.google.com and search"]
    #
    print(peek(None, None, TestMsg()).title)

if __name__ == "__main__":
    test_all()
