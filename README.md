# Overlastgebieden - import

## Development
	virtualenv -p /usr/local/bin/python3 ~/venv/overlastgebieden
    source ~/venv/overlastgebieden/bin/activate

    pip install -r requirements.txt

    # Lookup the objectstore password in Rattic
    export BAG_BRK_OBJECTSTORE_PASSWORD=xxxx

    # start database
    docker-compose up -d database

    # run import
    docker-compose build && docker-compose run app make runimport

    # development in docker
    # source files kunnen in eigen IDE geedit worden, import draait in docker
    docker-compose run -v "$PWD"/overlastgebieden:/app/overlastgebieden app bash
    make runimport

    # cleanup
    docker-compose down

    # database inladen vanuit acceptatie
    docker-compose exec database update-db.sh overlastgebieden


