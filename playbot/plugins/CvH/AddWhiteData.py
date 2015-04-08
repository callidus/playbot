
import os
import sys

import DataSource
from future import print_function  # noqa

db = DataSource.DataSource()
if os.path.isfile("./cvh.db"):
    db.openDB("./cvh.db")
else:
    db.buildDB("./cvh.db")


with open(sys.argv[1], 'r') as f:
    data = f.read()
    items = data.split("<>")
    for key, item in enumerate(items):
        try:
            db.addWhiteCard(key, item)
            print("{0} {1} ... OK".format(key, item))
        except Exception:
            print("{0} {1} ... FAIL".format(key, item))
