# overlastgebieden

## Development
	virtualenv -p /usr/local/bin/python3 ~/venv/overlastgebieden
    source ~/venv/overlastgebieden/bin/activate

    pip install -r requirements.txt

    export DEBUG=True
    export ZORGNED_USERNAME=dummy_user
    export ZORGNED_PASSWORD=dummy_password
    export ZORGNED_URL_VERSTREKKINGENADMINISTRATIE=http://localhost:8085/Verstrekkingenadministratie_V5
    export ZORGNED_URL_DOCUMENTEN=http://localhost:8085/Documenten_V1
    export TMA_CERTIFICATE=$(cat tests/saml/cert.txt)

    # Lookup the objectstore password in Rattic
    export INTEGRAAL_KLANTBEELD_OBJECTSTORE_PASSWORD=xxxx
