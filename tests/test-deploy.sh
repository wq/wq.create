#!/bin/bash
set -e

# Cleanup and initialize
rm -rf test_project
rm -rf output
mkdir output

if [[ "$TEST_VARIANT" == "postgis" ]]; then
    export DJANGO_SETTINGS_MODULE="test_project.settings.prod"
    GIS_FLAG="--with-gis"
elif [[ "$TEST_VARIANT" == "spatialite" ]]; then
    GIS_FLAG="--with-gis"
else
    # FIXME: Support testing non-gis build
    GIS_FLAG="--with-gis"
fi;


MANAGE="db/manage.py"
OUTPUT="../output"
COMPARE="../json-compare.py"
PORT=8000

# wq create: Create new project
rm -rf test_project

if [[ "$TEST_VARIANT" == "npm" ]]; then
    NPM_FLAG="--with-npm"
else
    NPM_FLAG="--without-npm"
fi;

wq create test_project ./test_project -d test.wq.io -t "test Project" $NPM_FLAG $GIS_FLAG
cd test_project

# Verify ./deploy.sh works
./deploy.sh 0.0.0

# Load db and verify initial config
if [[ "$TEST_VARIANT" == "postgis" ]]; then
    sed -i "s/'USER': 'test_project'/'USER': '$USER'/" db/test_project/settings/prod.py
    sed -i "s/ALLOWED_HOSTS.*/ALLOWED_HOSTS = ['localhost']/" db/test_project/settings/prod.py
else
    # See https://code.djangoproject.com/ticket/32935
    $MANAGE shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
fi;
$MANAGE migrate
$MANAGE dump_config > $OUTPUT/config0.json
$COMPARE expected/config0.json output/config0.json

# Remove example app and verify deploy still works
rm -rf db/test_project_survey/
sed -i 's/"test_project_survey",//' db/test_project/settings/base.py
./deploy.sh 0.0.1
$MANAGE migrate
$MANAGE dump_config > $OUTPUT/config1.json
$COMPARE expected/config1.json output/config1.json

# wq addform: Add a single form and verify changed config
wq addform -f ../location.csv
sed -i "s/class Meta:/def __str__(self):\n        return self.name\n\n    class Meta:/" db/location/models.py
$MANAGE dump_config > $OUTPUT/config2.json
$COMPARE expected/config2.json output/config2.json

# wq addform: Add a second form that references the first
wq addform -f ../observation.csv
sed -i "s/class Meta:/def __str__(self):\n        return '%s on %s' % (self.location, self.date)\n\n    class Meta:/" db/observation/models.py
$MANAGE dump_config > $OUTPUT/config3.json
$COMPARE expected/config3.json output/config3.json

# Enable anonymous submissions and start webserver
sed -i "s/WSGI_APPLICATION/ANONYMOUS_PERMISSIONS = ['location.add_location', 'observation.add_observation']\n\nWSGI_APPLICATION/" db/test_project/settings/base.py
$MANAGE runserver $PORT & sleep 5

# Submit a new site
curl -sf http://localhost:$PORT/locations.json > $OUTPUT/locations1.json
$COMPARE expected/locations1.json output/locations1.json
curl -sf http://localhost:$PORT/locations.json -d name="Site 1" -d type="water" -d geometry='{"type": "Point", "coordinates": [-93.28, 44.98]}' > /dev/null
curl -sf http://localhost:$PORT/locations.geojson > $OUTPUT/locations2.geojson
$COMPARE expected/locations2.geojson output/locations2.geojson

# Submit a new observation
curl -sf http://localhost:$PORT/observations.json -F location_id=1 -F date="2015-10-08" -F notes="A cold winter day in Minneapolis" -F photo=@../photo.jpg > /dev/null
curl -sf http://localhost:$PORT/observations.json > $OUTPUT/observations1.json
sed -i "s/$PORT/8000/" $OUTPUT/observations1.json
$COMPARE expected/observations1.json output/observations1.json
diff ../photo.jpg media/observations/photo.jpg
