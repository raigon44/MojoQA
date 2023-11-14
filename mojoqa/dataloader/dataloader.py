import json

import requests
from mojoqa.config.config import CFGLog
from mojoqa.utils.config import Config
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader
from langchain.schema import Document
from mojoqa.utils.logger import logger
import os


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

    @staticmethod
    def get_html_page_data(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error while accessing the url {url}. Return code {e.response.status_code}")
            raise

    def get_relevant_links(self, sub_page_page_url, base_url):
        html_data = self.get_html_page_data(sub_page_page_url)
        soup = BeautifulSoup(html_data, "html.parser")
        list_links = []
        dict_href_links = {}
        for link in soup.find_all("a", href=True):

            # Append to list if new link contains original link
            if str(link["href"]).startswith((str(sub_page_page_url))):
                list_links.append(link["href"])

            # Include all href that do not start with website link but with "../"
            if str(link["href"]).startswith("../"):
                if link["href"] not in dict_href_links:
                    print(link["href"])
                    dict_href_links[link["href"]] = None
                    link_with_www = base_url + link["href"][1:]
                    print("adjusted link =", link_with_www)
                    list_links.append(link_with_www)

        # Convert list of links to dictionary and define keys as the links and the values as "Not-checked"
        dict_links = dict.fromkeys(list_links, "Not-checked")
        return dict_links

    def get_sub_page_links(self, home_page_url, base_url) -> dict:
        link_dict = {home_page_url: "Not-checked"}
        for link in link_dict:
            if link_dict[link] == "Not-checked":
                dict_links_subpages = self.get_relevant_links(link, base_url)
                link_dict[link] = "Checked"
            else:
                dict_links_subpages = {}

            link_dict = {**dict_links_subpages, **link_dict}

        return link_dict

    def save_docs_to_json(self, array_of_docs):
        with open(self.data_config.mojo_docs_dataset_path, 'w') as json_fp:
            for doc in array_of_docs:
                json_fp.write(doc.json() + '\n')

    def load_docs_from_json(self):
        array_of_docs = []
        with open(self.data_config.mojo_docs_dataset_path, 'r') as json_fp:
            for line in json_fp:
                data = json.loads(line)
                obj = Document(**data)
                array_of_docs.append(obj)
        return array_of_docs

    def create_mojo_docs_dataset(self, home_page_url: str, base_url: str):
        logger.info("Creating Mojo Docs dataset by scrapping from the official Mojo documentation page")
        relevant_links_dict = self.get_sub_page_links(home_page_url, base_url)

        url_loader = UnstructuredURLLoader(urls=list(relevant_links_dict.keys()))
        html_doc = url_loader.load()

        if html_doc:
            logger.info("Mojo documents scrapped successfully!!")

        logger.info("Try to save the scrapped documents locally as a JSON file..")
        self.save_docs_to_json(html_doc)

        if os.path.isfile(self.data_config.mojo_docs_dataset_path):
            logger.info(f"Saved the dataset as JSON file successfully at {self.data_config.mojo_docs_dataset_path}")

        return html_doc

    def load_mojo_docs_dataset(self):

        logger.info(f"Checking if the dataset is locally available at {self.data_config.mojo_docs_dataset_path}")
        if os.path.isfile(self.data_config.mojo_docs_dataset_path):
            logger.info(f"Data file is locally available at {self.data_config.mojo_docs_dataset_path}. Loading the dataset...")
            return self.load_docs_from_json()
        else:
            logger.info(f"Mojo Docs not available locally at {self.data_config.mojo_docs_dataset_path}")
            return self.create_mojo_docs_dataset(self.data_config.mojo_documentation_home_url,
                                                 self.data_config.mojo_documentation_base_url)


if __name__ == "__main__":
    config = Config.from_json(CFGLog)
    data_obj = DataLoader(config.data)
    data_frame = data_obj.create_mojo_docs_dataset(
        'https://docs.modular.com/mojo/', 'https://docs.modular.com/')
    print(len(data_frame))
    data_frame.to_csv('data.csv')
