Elijah Thomas ethomas7@uoregon.edu

CS 322 Project 6

Project 5 implementation without direct connection between flask_brevets.py and MongoDB - instead, this is
achieved using a connection from flask_brevets to another service, under hostname api according to Docker.

See comments on these files in the /api folder for details on the changes and implementation:

	/api/databases/models.py	-	MongoEngine schemata definitions
	/api/resources/brevet.py	-	Brevet resource
	/api/resources/brevets.py	-	Brevets resource, distinct from the first one; the first resource is for
									acting on single brevets respective of their IDs; this one is for enacting
									protocols on ALL brevets irrespective of their IDs.

	/brevets/templates/calc.html	-	JSON formatting and handling modified, routing to brevets service changed
	/brevets/flask_brevets.py		-	_submit and _retrieve routes changed; truncated; much easier access to
										database now through API. Now uses requests module

	/brevets/requirements.txt	-	Added requests to pip requirements list