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
    create_view()
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

    cur.execute('SELECT count(*) FROM "geo_overlastgebieden";')
    result = cur.fetchone()
    if result[0] < 30:
        raise Exception("Too little records in database, import failed.")

    cur.close()
    conn.close()
    print('Import successfull')


def create_view():
    print('Create view')
    conn = psycopg2.connect(settings.PG_LOGIN)
    cur = conn.cursor()
    try:
        cur.execute("""DROP MATERIALIZED VIEW IF EXISTS geo_overlastgebieden;""")
        cur.execute("""
                    CREATE MATERIALIZED VIEW geo_overlastgebieden AS
                    SELECT
                      oov."OOV_NAAM" as id,
                      oov."OOV_NAAM" as naam,
                      oov."OOV_NAAM" as display,
                      cast('overlastgebieden/overlastgebied' as varchar(50)) as type,
                      oov."TYPE" as overlastgebied_type,
                        cast('' as varchar(50)) as uri,
                      oov."geom" AS geometrie
                    FROM
                      "OOV_gebieden_totaal" as oov;
                    """)
        cur.execute("""
                    CREATE INDEX index_geo_overlastgebieden_gist
                      ON geo_overlastgebieden USING
                      gist(geometrie)
                    """)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print('Error during create view. ', e)
        raise e
    finally:
        cur.close()
        conn.close()
        print('Create view successfull')
