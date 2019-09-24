#!/bin/bash
set -e

# Cleanup and initialize
rm -rf test_project
rm -rf output
mkdir output

MANAGE="test_project/db/manage.py"
PORT=8001

# wq start: Create new project and verify empty config
rm -rf test_project
wq start test_project
$MANAGE migrate
$MANAGE dump_config > output/config1.json
./json-compare.py expected/config1.json output/config1.json

# wq addform: Add a single form and verify changed config
cd test_project/db
wq addform -f ../../location.csv
sed -i "s/class Meta:/def __str__(self):\n        return self.name\n\n    class Meta:/" location/models.py
cd ../../
$MANAGE dump_config > output/config2.json
./json-compare.py expected/config2.json output/config2.json

# wq addform: Add a second form that references the first
cd test_project/db
wq addform -f ../../observation.csv
sed -i "s/class Meta:/def __str__(self):\n        return '%s on %s' % (self.location, self.date)\n\n    class Meta:/" observation/models.py
cd ../../
$MANAGE dump_config > output/config3.json
./json-compare.py expected/config3.json output/config3.json

# Enable anonymous submissions and start webserver
sed -i "s/WSGI_APPLICATION/ANONYMOUS_PERMISSIONS = ['location.add_location', 'observation.add_observation']\n\nWSGI_APPLICATION/" test_project/db/test_project/settings/base.py
$MANAGE runserver $PORT & sleep 5

# Submit a new site
curl -sf http://localhost:$PORT/locations.json > output/locations1.json
./json-compare.py expected/locations1.json output/locations1.json
curl -sf http://localhost:$PORT/locations.json -d name="Site 1" -d type="water" -d geometry='{"type": "Point", "coordinates": [-93.28, 44.98]}' > /dev/null
curl -sf http://localhost:$PORT/locations.geojson > output/locations2.geojson
./json-compare.py expected/locations2.geojson output/locations2.geojson

# Submit a new observation
curl -sf http://localhost:$PORT/observations.json -F location_id=1 -F date="2015-10-08" -F notes="A cold winter day in Minneapolis" -F photo=@photo.jpg > /dev/null
curl -sf http://localhost:$PORT/observations.json > output/observations1.json
sed -i "s/$PORT/8000/" output/observations1.json
./json-compare.py expected/observations1.json output/observations1.json
diff photo.jpg test_project/media/observations/photo.jpg
