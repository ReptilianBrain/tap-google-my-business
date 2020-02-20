import singer
import json
import sys
from tap_google_my_business.discover import discover_streams
from tap_google_my_business.sync import sync_stream

from singer import metadata

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


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = args.config

    if args.discover:
        do_discover(args.config)
    elif args.catalog:
        do_sync(config, args.catalog, args.state)


if __name__ == '__main__':
    main()