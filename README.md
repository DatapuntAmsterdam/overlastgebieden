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
    docker-compose run app make runimport

    # cleanup
    docker-compose down

