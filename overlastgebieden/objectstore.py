"""Retrieve file from remote objectstore.

"""
import logging
import os
from functools import lru_cache
from dateutil import parser
from swiftclient.client import Connection
from .settings import OBJECTSTORE_CONFIG as config

log = logging.getLogger(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

os_connect = {
    'auth_version': '2.0',
    'authurl': 'https://identity.stack.cloudvps.com/v2.0',
    'user': config['user'],
    'key': config['key'],
    'tenant_name': config['tenant_name'],
    'os_options': {
        'tenant_id': config['tenant_id'],
        'region_name': 'NL',
    }
}


@lru_cache(maxsize=None)
def get_conn():
    return Connection(**os_connect)


def copy_file_from_objectstore(container, file_name, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    destination = download_dir + file_name
    log.info("Download file {} to {}".format(file_name, destination))
    conn = get_conn()
    headers = conn.head_object(container, file_name)
    last_modified = headers.get('last-modified')
    # print(last_modified)
    # Mon, 27 Aug 2018 21:55:46 GMT
    datetime_object = parser.parse(last_modified)
    epoch_time = int(datetime_object.timestamp())
    with open(destination, 'wb') as f:
        f.write(conn.get_object(container, file_name)[1])
    os.utime(destination, (epoch_time, epoch_time))
    return destination
