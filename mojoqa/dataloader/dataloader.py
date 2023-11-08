
import os
import requests
from urllib.parse import urljoin, urlparse
from mojoqa.config.config import CFGLog
from mojoqa.utils.config import Config


class DataLoader:
    """
    DataLoader class for loading and preprocessing data from Mojo documentation.
    """

    def __init__(self, data_config):
        """
        Initializes the DataLoader with a data configuration.

        Args:
            data_config: Configuration object containing data paths.
        """
        self.data_config = data_config

    def download_html_files_recursively(self, base_url, path):
        response = requests.get(base_url)
        os.makedirs(path, exist_ok=True)

        if response.status_code == 200:
            with open(os.path.join(path, "index.html"), "wb") as fp:
                fp.write(response.content)

        for link in response.text.split('href="')[1:]:
            link = link.split('"', 1)[0]
            if link.startswith(('http://', 'https://')):
                new_url = link
            else:
                new_url = urljoin(base_url, link)

            if urlparse(new_url).netloc == urlparse(base_url).netloc:
                self.download_html_files_recursively(new_url, os.path.join(path, urlparse(new_url).path.lstrip('/')))


if __name__ == "__main__":
    config = Config.from_json(CFGLog)
    data_obj = DataLoader(config.data)
    data_obj.download_html_files_recursively(config.data.mojo_documentation_base_url, config.data.raw_html_files_path)