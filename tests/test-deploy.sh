#!/bin/bash
set -e

# Cleanup
rm -rf test_project
rm -rf output
mkdir output

# wq start: Create new project and verify empty config
rm -rf test_project
wq start test_project
if [ `python -c 'import sys; print(sys.version_info[0])'` == "2" ]
then
   sed -i "s/python3/python/" test_project/db/manage.py
fi
test_project/db/manage.py dump_config > output/config1.json
./json-compare.py expected/config1.json output/config1.json

# wq addform: Add a single form and verify changed config
cd test_project/db
wq addform ../../location.csv
sed -i "s/class Meta:/def __str__(self):\n        return self.name\n\n    class Meta:/" location/models.py
sed -i "s/# Project apps/# Project apps\n    'location',/" test_project/settings.py
cd ../../
test_project/db/manage.py dump_config > output/config2.json
./json-compare.py expected/config2.json output/config2.json

# wq addform: Add a second form that references the first
cd test_project/db
wq addform ../../observation.csv
sed -i "s/class Meta:/def __str__(self):\n        return '%s on %s' % (self.location, self.date)\n\n    class Meta:/" observation/models.py
sed -i "s/'location',/'location',\n    'observation',/" test_project/settings.py
cd ../../
test_project/db/manage.py dump_config > output/config3.json
./json-compare.py expected/config3.json output/config3.json

# Create database tables
cd test_project/db
dropdb -Upostgres test_project --if-exists
createdb -Upostgres test_project
psql -Upostgres test_project -c "CREATE EXTENSION postgis";
sed -i "s/'USER': 'test_project'/'USER': 'postgres'/" test_project/local_settings.py
./manage.py makemigrations location observation
./manage.py migrate
cd ../../

# Enable anonymous submissions and start webserver
cd test_project/db
sed -i "s/WSGI_APPLICATION/ANONYMOUS_PERMISSIONS = ['location.add_location', 'observation.add_observation']\n\nWSGI_APPLICATION/" test_project/settings.py
./manage.py runserver & sleep 5
cd ../../

# Submit a new site
curl -sf http://localhost:8000/locations.json > output/locations1.json
./json-compare.py expected/locations1.json output/locations1.json
curl -sf http://localhost:8000/locations.json -d name="Site 1" -d type="water" -d geometry='{"type": "Point", "coordinates": [-93.28, 44.98]}' > /dev/null
curl -sf http://localhost:8000/locations.geojson > output/locations2.geojson
./json-compare.py expected/locations2.geojson output/locations2.geojson

# Submit a new observation
curl -sf http://localhost:8000/observations.json -F location_id=1 -F date="2015-10-08" -F notes="A cold winter day in Minneapolis" -F photo=@photo.jpg > /dev/null
curl -sf http://localhost:8000/observations.json > output/observations1.json
./json-compare.py expected/observations1.json output/observations1.json
diff photo.jpg test_project/media/observations/photo.jpg
