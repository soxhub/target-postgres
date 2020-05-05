from singer import utils
import psycopg2

from target_postgres.postgres import MillisLoggingConnection, PostgresTarget
from target_postgres import target_tools
from os import path

REQUIRED_CONFIG_KEYS = [
    'postgres_database'
]

def getPostgresTarget(config, input_stream=None):
 with psycopg2.connect(
            connection_factory=MillisLoggingConnection,
            host=config.get('postgres_host', 'localhost'),
            port=config.get('postgres_port', 5432),
            dbname=config.get('postgres_database'),
            user=config.get('postgres_username'),
            password=config.get('postgres_password'),
            sslmode=config.get('postgres_sslmode'),
            sslcert=config.get('postgres_sslcert'),
            sslkey=config.get('postgres_sslkey'),
            sslrootcert=config.get('postgres_sslrootcert'),
            sslcrl=config.get('postgres_sslcrl')
    ) as connection:
        postgres_target = PostgresTarget(
            connection,
            postgres_schema=config.get('postgres_schema', 'public'),
            logging_level=config.get('logging_level'),
            persist_empty_tables=config.get('persist_empty_tables'),
            add_upsert_indexes=config.get('add_upsert_indexes', True),
            before_run_sql=config.get('before_run_sql'),
            after_run_sql=config.get('after_run_sql'),
        )

        return postgres_target


def main(config, input_stream=None):
    target_postgres = getPostgresTarget(config);

    if input_stream:
        target_tools.stream_to_target(input_stream, postgres_target, config=config)
    else:
        target_tools.main(postgres_target)

def write_state():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    postgres_target = getPostgresTarget(args.config)
    state_location = args.config.get('state_location')

    if state_location and path.exists(state_location):
        postgres_target.write_state(state_location)
    else:
        print("No State File. Skip!")

def read_state():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    postgres_target = getPostgresTarget(args.config)
    print(args.config)
    state_location = args.config.get('destination_state_location')
    if state_location:
        postgres_target.read_state(state_location)
    else:
        print("No State Location. Skip!")

def cli():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    main(args.config)
