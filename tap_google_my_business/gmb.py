import singer

from googleapiclient import sample_tools

# https://developers.google.com/my-business/samples
# https://developers.google.com/my-business/samples/mybusiness_google_rest_v4p5.json
DISCOVERY_DOC = "gmb_discovery.json"

LOGGER = singer.get_logger()


class GoogleMyBusiness:
    arg = []

    def __init__(self, account, key_file_location, credentials_location):
        self.service, flag = sample_tools.init(
            self.arg,
            name=f"{credentials_location}mybusiness",
            version="v4",
            doc=__doc__,
            filename=key_file_location,
            scope="https://www.googleapis.com/auth/business.manage",
            discovery_filename=f"{credentials_location}gmb_discovery.json"
        )
        self.account = account

    def get_locations(self):
        try:
            has_page_token = True
            page_token = None
            while has_page_token:
                locations_list = self.service.accounts().locations().list(
                    parent=self.account,
                    pageToken=page_token).execute()

                yield locations_list['locations']

                page_token = locations_list.get('nextPageToken')
                has_page_token = page_token is not None

        except Exception as err:
            LOGGER.error(err)
