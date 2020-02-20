import json
from pathlib import Path
import sys

import singer
from singer import metadata


LOGGER = singer.get_logger()

def discover_streams(config):
    default_catalog = Path(__file__).parent.joinpath('defaults', 'default_catalog.json')

    catalog_def_file = config.get('streams', default_catalog)

    if Path(catalog_def_file).is_file():
        try:
            catalog_definition = load_json(catalog_def_file)
        except ValueError:
            LOGGER.critical(
                f"tap-google-analytics: The JSON definition in '{catalog_def_file}' has errors"
            )
            sys.exit(1)
    else:
        LOGGER.critical(f"tap-google-analytics: '{catalog_def_file}' file not found")
        sys.exit(1)

    return catalog_definition['streams']


def load_metadata(table_spec, schema):
    mdata = metadata.new()

    mdata = metadata.write(mdata, (), 'table-key-properties', table_spec['key_properties'])

    for field_name in schema.get('properties', {}).keys():
        if table_spec.get('key_properties', []) and field_name in table_spec.get('key_properties', []):
            mdata = metadata.write(mdata, ('properties', field_name), 'inclusion', 'automatic')
        else:
            mdata = metadata.write(mdata, ('properties', field_name), 'inclusion', 'available')

    return metadata.to_list(mdata)


def load_json(path):
    with open(path) as f:
        return json.load(f)