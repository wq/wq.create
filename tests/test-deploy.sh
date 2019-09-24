#!/bin/bash
set -e

# Cleanup and initialize
rm -rf test_project
rm -rf output
mkdir output

if [ "$POSTGRES" ]; then
    dropdb -Upostgres test_project --if-exists
    createdb -Upostgres test_project
    psql -Upostgres test_project -c "CREATE EXTENSION postgis";

    export DJANGO_SETTINGS_MODULE="test_project.settings.prod"
fi;

MANAGE="test_project/db/manage.py"
PORT=8000

# wq start: Create new project
rm -rf test_project

GIS_FLAG="--with-gis"

if [ "$WITH_NPM" ]; then
    NPM_FLAG="--with-npm --npm-install"
else
    NPM_FLAG="--without-npm"
fi;

wq start test_project ./test_project -d test.wq.io -i io.wq.test $NPM_FLAG $GIS_FLAG

# Verify ./deploy.sh works
cd test_project
mkdir -p .wq-pgb
echo "disable: true" > .wq-pgb/wq-pgb.yml
./deploy.sh 0.0.0
cd ..;

# Load db and verify initial config
if [ "$POSTGRES" ]; then
    sed -i "s/'USER': 'test_project'/'USER': 'postgres'/" test_project/db/test_project/settings/prod.py
    sed -i "s/ALLOWED_HOSTS.*/ALLOWED_HOSTS = ['localhost']/" test_project/db/test_project/settings/prod.py
fi;
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
