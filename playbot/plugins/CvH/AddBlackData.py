
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
        slots = item.count("__________")
        try:
            db.addBlackCard(key, slots, item)
            print("{0} {1} {2} ... OK".format(key, item, slots))
        except Exception:
            print("{0} {1} {2} ... FAIL".format(key, item, slots))
