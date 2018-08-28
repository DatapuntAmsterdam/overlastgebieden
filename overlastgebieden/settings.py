import os
import re


def get_docker_host():
    """
    Looks for the DOCKER_HOST environment variable to find the VM
    running docker-machine.

    If the environment variable is not found, it is assumed that
    you're running docker on localhost.
    """
    d_host = os.getenv('DOCKER_HOST', None)
    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)
    return 'localhost'


def in_docker():
    """
    Checks pid 1 cgroup settings to check with reasonable certainty we're in a
    docker env.
    :return: true when running in a docker container, false otherwise
    """
    try:
        cgroup = open('/proc/1/cgroup', 'r').read()
        return ':/docker/' in cgroup or ':/docker-ce/' in cgroup
    except IOError:
        return False


OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'


class Location_key:
    local = 'local'
    docker = 'docker'
    override = 'override'


def get_database_key():
    if os.getenv(OVERRIDE_HOST_ENV_VAR):
        return Location_key.override
    elif in_docker():
        return Location_key.docker

    return Location_key.local


DATABASE_OPTIONS = {
    Location_key.docker: {
        'NAME': os.getenv('DATABASE_NAME', 'overlastgebieden'),
        'USER': os.getenv('DATABASE_USER', 'overlastgebieden'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    Location_key.local: {
        'NAME': os.getenv('DATABASE_NAME', 'overlastgebieden'),
        'USER': os.getenv('DATABASE_USER', 'overlastgebieden'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5442'
    },
    Location_key.override: {
        'NAME': os.getenv('DATABASE_NAME', 'overlastgebieden'),
        'USER': os.getenv('DATABASE_USER', 'overlastgebieden'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

ENGINE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    DATABASES['default']['USER'],
    DATABASES['default']['PASSWORD'],
    DATABASES['default']['HOST'],
    DATABASES['default']['PORT'],
    DATABASES['default']['NAME']
)

OGR_PG_LOGIN = "host={} port={} dbname={} user={} password={}".format(
    DATABASES['default']['HOST'],
    DATABASES['default']['PORT'],
    DATABASES['default']['NAME'],
    DATABASES['default']['USER'],
    DATABASES['default']['PASSWORD'])

PG_LOGIN = "host={} port={} dbname={} user={} password={}".format(
    DATABASES['default']['HOST'],
    DATABASES['default']['PORT'],
    DATABASES['default']['NAME'],
    DATABASES['default']['USER'],
    DATABASES['default']['PASSWORD'])


assert os.getenv('BAG_BRK_OBJECTSTORE_PASSWORD')

OBJECTSTORE_CONFIG = {
    'user': 'bag_brk',
    'key': os.getenv('BAG_BRK_OBJECTSTORE_PASSWORD', 'insecure'),
    'tenant_name': 'BGE000081_BAG',
    'tenant_id': '4f2f4b6342444c84b3580584587cfd18',
}
