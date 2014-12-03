
import os
import sys
import DataSource

db = DataSource.DataSource()
if os.path.isfile( "./cvh.db" ):
	db.openDB( "./cvh.db" )
else: 
	db.buildDB( "./cvh.db" )	

with open( sys.argv[1], 'r') as f:
	data = f.read()
	items = data.split( "<>" )
	for key,item in enumerate( items ):
		slots = item.count( "__________" )
		print key, item, slots,
		try:
			db.addBlackCard( key, slots, item )
			print "... OK"
		except:
			print "... Fail"