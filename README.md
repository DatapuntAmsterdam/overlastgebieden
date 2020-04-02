# Overlastgebieden - import

Importeren van de overlastgebieden kaartlaag.
Input is een shapefile, deze wordt geimporteerd in de overlastgebieden database
en met een view beschikbaar gesteld voor de mapserver.

## Development
	virtualenv -p /usr/local/bin/python3 ~/venv/overlastgebieden
    source ~/venv/overlastgebieden/bin/activate

    pip install -r requirements.txt

    # Lookup the objectstore password in Rattic
    export VSD_OBJECTSTORE_PASSWORD=xxxx

    # start database
    docker-compose up -d database

    # run import
    docker-compose build && docker-compose run app make runimport

    # run import - voor lokale ontwikkeling
    # de bron code kan in eigen omgeving geedit worden, 
    # waarna de import gedraaid wordt.
    
    docker-compose run -v "$PWD"/overlastgebieden:/app/overlastgebieden app bash
    make runimport

    # cleanup
    docker-compose down

    # database inladen vanuit acceptatie
    docker-compose exec database update-db.sh overlastgebieden


