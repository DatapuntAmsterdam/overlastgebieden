"""Import shape file. Fill the database.

"""

from overlastgebieden import objectstore, settings
import subprocess
import psycopg2


def run_import():
    container = 'Diva/gebieden_shp'
    download_dir = '/tmp/overlastgebieden/'

    objectstore.copy_file_from_objectstore(container=container,
                                           download_dir=download_dir,
                                           file_name="OOV_gebieden_totaal.dbf")

    objectstore.copy_file_from_objectstore(container=container,
                                           download_dir=download_dir,
                                           file_name="OOV_gebieden_totaal.shx")

    file = objectstore.copy_file_from_objectstore(
        container=container,
        download_dir=download_dir,
        file_name="OOV_gebieden_totaal.shp")

    convert_shape_to_postgres(file, settings.OGR_PG_LOGIN)
    check_import()


def convert_shape_to_postgres(filename, org_pg_login):
    print('Converting ', filename)
    command = (
        'ogr2ogr -nlt PROMOTE_TO_MULTI -progress '
        '-f "PostgreSQL" '
        'PG:"{PG}" -gt 655360 -s_srs "EPSG:28992" -t_srs '
        '"EPSG:28992" {LCO} {CONF} {FNAME}'.format(
            PG=org_pg_login,
            LCO='-lco SPATIAL_INDEX=OFF -lco PRECISION=NO -lco '
                'LAUNDER=NO -lco GEOMETRY_NAME=geom',
            CONF='--config PG_USE_COPY YES',
            FNAME=filename
        )
    )

    subprocess.call(command, shell=True)


def check_import():
    print('Check import')
    conn = psycopg2.connect(settings.PG_LOGIN)
    cur = conn.cursor()
    cur.execute('SELECT count(*) FROM "OOV_gebieden_totaal";')
    result = cur.fetchone()
    if result[0] < 30:
        raise Exception("Too little records in database, import failed.")
    cur.close()
    conn.close()
    print('Import successfull')
