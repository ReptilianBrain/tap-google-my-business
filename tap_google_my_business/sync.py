from datetime import datetime, timezone

import singer
from singer import utils

from tap_google_my_business.gmb import GoogleMyBusiness

LOGGER = singer.get_logger()

def custom_stream(state, stream, config):
    table_name = stream.tap_stream_id
    records_streamed = 0
    now = datetime.now(timezone.utc).isoformat()

    gmb = GoogleMyBusiness(config['accounts'],
                           config['credentials_file_location']
                           )

    for locations in gmb.get_locations():
        singer.write_records(table_name, locations)
        records_streamed += len(locations)

        state = singer.write_bookmark(state, table_name, 'updated_at', now)
        state = singer.write_bookmark(state, table_name, 'location_count', records_streamed)
        singer.write_state(state)

    return records_streamed


def sync_stream(config, state, stream):
    table_name = stream.tap_stream_id
    modified_since = utils.strptime_with_tz(singer.get_bookmark(state, table_name, 'updated_at') or
                                            config['start_date'])

    LOGGER.info(f'Syncing table [{table_name}].')
    LOGGER.info('Getting files modified since %s.', modified_since)

    records_streamed = custom_stream(state, stream, config)

    LOGGER.info('Wrote %s records for table "%s".', records_streamed, table_name)

    return records_streamed
