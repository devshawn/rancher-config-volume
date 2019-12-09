import os
import sys
from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Generator:
    def __init__(self):
        retries = Retry(total=6, backoff_factor=0.5, status_forcelist=[502, 503, 504, 500, 404])
        self.command = self.get_command()
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.run_forever = os.environ.get("RANCHER_RUN_FOREVER", "true") == "true"
        self.base_url = os.environ.get("RANCHER_METADATA_HOST", "rancher-metadata")

    @staticmethod
    def get_command():
        try:
            return sys.argv[1].strip().strip("/")
        except IndexError:
            print("Error: configuration key required. Please pass it as an argument.")
            sys.exit(1)

    def make_metadata_request(self, suffix):
        try:
            url = "http://{}/2015-07-25/self/service/metadata/{}".format(self.base_url, suffix)
            result = self.session.get(url)
            if result.status_code == 200:
                return result
            else:
                raise Exception("Received non-200 status code: {}".format(result.status_code))
        except Exception as ex:
            print("Exception when making request: {}".format(ex))
            sys.exit(1)

    def get_config_path(self, key):
        result = self.make_metadata_request("{}/path".format(key))
        return result.text.strip()

    def get_config_content(self, key):
        result = self.make_metadata_request("{}/content".format(key))
        return result.text.strip() + "\n"

    def execute(self):
        print("Creating config file for key: {}".format(self.command))
        path = self.get_config_path(self.command)
        content = self.get_config_content(self.command)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            f.write(content)

        print("Wrote config file to path: {}".format(path))

        if self.run_forever:
            while not sleep(5):
                pass


def main():
    Generator().execute()


if __name__ == "__main__":
    main()
