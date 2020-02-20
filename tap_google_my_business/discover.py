from singer import metadata


def discover_streams(config):
    streams = [
        {
            "tap_stream_id": "users",
            "stream": "users",
            "schema": {
                "type": ["null", "object"],
                "additionalProperties": False,
                "properties": {
                    "ip": {"type": "string"},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "id": {"type": "integer"}
                }
            }
        }
    ]

    return streams


def load_metadata(table_spec, schema):
    mdata = metadata.new()

    mdata = metadata.write(mdata, (), 'table-key-properties', table_spec['key_properties'])

    for field_name in schema.get('properties', {}).keys():
        if table_spec.get('key_properties', []) and field_name in table_spec.get('key_properties', []):
            mdata = metadata.write(mdata, ('properties', field_name), 'inclusion', 'automatic')
        else:
            mdata = metadata.write(mdata, ('properties', field_name), 'inclusion', 'available')

    return metadata.to_list(mdata)
