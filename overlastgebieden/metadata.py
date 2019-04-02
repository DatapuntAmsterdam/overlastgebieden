import datetime
import logging
import requests
import os


log = logging.getLogger(__name__)


def upload(dataset_id, year, month, day):
    metadata_url = os.getenv('METADATA_URL')
    if metadata_url is None or len(metadata_url) == 0:
        ENVIRONMENT = os.getenv('ENVIRONMENT')
        if ENVIRONMENT == 'acceptance' or ENVIRONMENT == 'production':
            acc = 'acc.' if ENVIRONMENT == 'acceptance' else ''
            metadata_url = f'https://{acc}api.data.amsterdam.nl/metadata/'

    if metadata_url is None or len(metadata_url) == 0:
        log.warning("METADATA_URL is not set, won't upload dataset modification "
                    "date. This should only happen during tests!")
        return

    if metadata_url[-1] != '/':
        metadata_url += '/'

    dsid = dataset_id.lower()

    uri = '{}{}/'.format(metadata_url, dsid)

    moddate = '{}-{}-{}'.format(year, month, day)
    datetime.datetime.strptime(moddate, '%Y-%m-%d')

    return requests.put(uri, {
        'id': dsid,
        'data_modified_date': moddate,
        'last_import_date': datetime.date.today(),
    })
