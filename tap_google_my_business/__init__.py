from pathlib import Path
import json
import sys

import singer
from singer import metadata

from tap_google_my_business.discover import discover_streams
from tap_google_my_business.sync import sync_stream

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = ["accounts", "start_date"]
KEY_PROPERTIES = ["name"]


def do_discover(config):
    LOGGER.info("Starting discover")
    streams = discover_streams(config)
    if not streams:
        raise Exception("No streams found")
    catalog = {"streams": streams}
    json.dump(catalog, sys.stdout, indent=2)
    LOGGER.info("Finished discover")


def do_sync(config, catalog, state):
    LOGGER.info('Starting sync.')

    for stream in catalog.streams:
        raw_mdata = metadata.get_standard_metadata(
            schema=stream.schema.to_dict(),
            key_properties=KEY_PROPERTIES
        )
        mdata = metadata.to_map(raw_mdata)

        singer.write_state(state)
        key_properties = metadata.get(mdata, (), 'table-key-properties')
        singer.write_schema(stream.tap_stream_id, stream.schema.to_dict(), key_properties)

        LOGGER.info("%s: Starting sync", stream.tap_stream_id)
        counter_value = sync_stream(config, state, stream)
        LOGGER.info("%s: Completed sync (%s rows)", stream.tap_stream_id, counter_value)

    LOGGER.info('Done syncing.')


def process_args():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    if not args.config.get('key_file_location'):
        LOGGER.critical("tap-google-my-business: a valid key_file_location string must be provided.")
        sys.exit(1)

    if not args.config.get('credentials_location'):
        LOGGER.critical("tap-google-my-business: a valid credentials_location string must be provided.")
        sys.exit(1)

    if Path(args.config['key_file_location']).is_file():
        try:
            args.config['client_secrets'] = load_json(args.config['key_file_location'])
        except ValueError:
            LOGGER.critical(f"tap-google-my-business: The JSON definition in [{args.config['credentials_file_location']}] has errors")
            sys.exit(1)
    else:
        LOGGER.critical(f"tap-google-my-business: '{args.config['key_file_location']}' file not found")
        sys.exit(1)

    if not Path(args.config['credentials_file_location']):
        LOGGER.critical(f"tap-google-my-business: '{args.config['credentials_file_location']}' not found")
        sys.exit(1)

    return args


def load_json(path):
    with open(path) as f:
        return json.load(f)


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = process_args()
    config = args.config

    if args.discover:
        do_discover(args.config)
    elif args.catalog:
        do_sync(config, args.catalog, args.state)


if __name__ == '__main__':
    main()
