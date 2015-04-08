import os
import re
import sys

import data_source
from future import print_function  # noqa

db = data_source.DataSource()
if os.path.isfile(sys.argv[1]):
    db.openDB(sys.argv[1])
else:
    db.buildDB(sys.argv[1])

with open(sys.argv[2], 'r') as f:
    data = f.read()
    items = data.split("\n")
    for key, item in enumerate(items):
        if len(item) != 0:
            item = item.replace("\n", " ")
            item = re.sub("[ \t]+", " ", item)
            print(key, item)
            try:
                db.addFortune(unicode(item, 'utf-8'))
                print("... OK")
            except Exception as e:
                print("... Fail", e)
