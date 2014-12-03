
import os
import sys
import DataSource

db = DataSource.DataSource()
if os.path.isfile( "./cvh.db" ):
	db.openDB( "./cvh.db" )
else: 
	db.buildDB( "./cvh.db" )	


with open( sys.argv[1], 'r' ) as f:
	data = f.read()
	items = data.split( "<>" )
	for key,item in enumerate( items ):
		print key, item,
		try:
			db.addWhiteCard( key, item )
			print " ... OK"
		except:
			print " ... FAIL"