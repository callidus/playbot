
from __future__ import absolute_import
from __future__ import print_function

import os
import re
import sys

from playbot.plugins.fortune import data_source


db = data_source.DataSource()
if os.path.isfile(sys.argv[1]):
    db.open_db(sys.argv[1])
else:
    db.build_db(sys.argv[1])

with open(sys.argv[2], 'r') as f:
    data = f.read()
    items = data.split("\n")
    for key, item in enumerate(items):
        if len(item) != 0:
            item = item.replace("\n", " ")
            item = re.sub("[ \t]+", " ", item)
            print(key, item)
            try:
                db.add_fortune(unicode(item, 'utf-8'))
                print("... OK")
            except Exception as e:
                print("... Fail", e)
