curl -O ftp://ftp2.census.gov/geo/tiger/TIGER2015/ROADS/tl_2015_06095_roads.zip
unzip tl_2015_06095_roads.zip

cd tl_2015_06095_roads
ogr2ogr -f GeoJSON tl_2015_06095_roads.json tl_2015_06095_roads.shp
cd ..

curl 'http://api.censusreporter.org/1.0/geo/show/tiger2013?geo_ids=140|16000US0681666' > census_tracts.json

python filter_roads.py census_tracts.json tl_2015_06095_roads/tl_2015_06095_roads.json > filtered_roads.txt
