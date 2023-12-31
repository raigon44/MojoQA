import json

import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader
from langchain.schema import Document
from mojoqa.utils.logger import logger
import os


class DataLoader:
    """
    DataLoader class for loading and preprocessing data from Mojo documentation.
    """

    def __init__(self, config):
        """
        Initializes the DataLoader with a data configuration.

        Args:
            config: Configuration object containing data paths & other congigurations.
        """
        self.config = config

    @staticmethod
    def get_html_page_data(url: str) -> str:
        """
        Fetches HTML data from the given URL.
        Args:
            url: The URL to fetch the HTML data from
        Returns:
            The html data in string format
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error while accessing the url {url}. Return code {e.response.status_code}")
            raise

    def get_relevant_links(self, sub_page_page_url: str, base_url: str) -> dict:
        """
        Extracts relevant links from a given sub-page URL.
        Args:
            sub_page_page_url (str): URL of the sub-page.
            base_url (str): Base URL for constructing complete URLs.
        Returns:
            dict: Dictionary of relevant links with initial status "Not-checked".
        """
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
        """
        Retrieves all relevant links from the home page and its sub-pages.

        Args:
            home_page_url (str): URL of the home page.
            base_url (str): Base URL for constructing complete URLs.

        Returns:
            dict: Dictionary of all relevant links with initial status "Not-checked".
        """
        link_dict = {home_page_url: "Not-checked"}
        for link in link_dict:
            if link_dict[link] == "Not-checked":
                dict_links_subpages = self.get_relevant_links(link, base_url)
                link_dict[link] = "Checked"
            else:
                dict_links_subpages = {}

            link_dict = {**dict_links_subpages, **link_dict}

        return link_dict

    @staticmethod
    def save_docs_to_json(array_of_docs, path):
        """
        Saves an array of Document objects to a JSON file.

        Args:
            array_of_docs (list): List of Document objects.
            path (str): Path to the output JSON file.
        """
        with open(path, 'w') as json_fp:
            for doc in array_of_docs:
                json_fp.write(doc.json() + '\n')

    @staticmethod
    def load_docs_from_json(path):
        """
        Loads Document objects from a JSON file.

        Args:
            path (str): Path to the input JSON file.

        Returns:
            list: List of Document objects.
        """
        array_of_docs = []
        with open(path, 'r') as json_fp:
            for line in json_fp:
                data = json.loads(line)
                obj = Document(**data)
                array_of_docs.append(obj)
        return array_of_docs

    def create_mojo_docs_dataset(self, home_page_url: str, base_url: str):
        """
        Creates a Mojo Docs dataset by scraping from the official Mojo documentation page.

        Args:
            home_page_url (str): URL of the home page.
            base_url (str): Base URL for constructing complete URLs.

        Returns:
            list: List of Document objects representing the scraped data.
        """
        logger.info("Creating Mojo Docs dataset by scrapping from the official Mojo documentation page")
        relevant_links_dict = self.get_sub_page_links(home_page_url, base_url)

        url_loader = UnstructuredURLLoader(urls=list(relevant_links_dict.keys()))
        html_doc = url_loader.load()

        if html_doc:
            logger.info("Mojo documents scrapped successfully!!")

        logger.info("Try to save the scrapped documents locally as a JSON file..")
        self.save_docs_to_json(html_doc, self.config.path.mojo_docs_dataset_path)

        if os.path.isfile(self.config.path.mojo_docs_dataset_path):
            logger.info(f"Saved the dataset as JSON file successfully at {self.config.path.mojo_docs_dataset_path}")

        return html_doc

    def create_mojo_docs_short_dataset(self, list_of_urls: list):
        """
        Creates a shorter Mojo Docs dataset by scraping a few HTML pages from the official Mojo documentation page.

        Args:
            list_of_urls (list): List of specific URLs to scrape.

        Returns:
            list: List of Document objects representing the scraped data.
        """
        logger.info(
            "Creating Mojo Docs dataset by scrapping only a few html pages from official mojo documentation page")

        url_loader = UnstructuredURLLoader(urls=list_of_urls)
        html_doc = url_loader.load()

        if html_doc:
            logger.info("Mojo documents scrapped successfully!!")

        logger.info("Try to save the scrapped documents locally as a JSON file..")
        self.save_docs_to_json(html_doc, self.config.path.mojo_docs_short_dataset_path)

        if os.path.isfile(self.config.path.mojo_docs_short_dataset_path):
            logger.info(
                f"Saved the dataset as JSON file successfully at {self.config.path.mojo_docs_short_dataset_path}")

        return html_doc

    def load_mojo_docs_dataset(self, dataset_variant: str):
        """
        Loads the Mojo Docs dataset based on the specified variant.

        Args:
            dataset_variant (str): 'short' for a shorter dataset, 'full' for the complete dataset.

        Returns:
            list: List of Document objects representing the loaded data.
        """
        logger.info(f'The dataset variant selected is {dataset_variant}')
        if dataset_variant == 'short':
            logger.info("Only a subset of mojo documentation will be extracted")
            dataset_path = self.config.path.mojo_docs_short_dataset_path
        else:
            logger.info("All the official mojo documentation will be used")
            dataset_path = self.config.path.mojo_docs_dataset_path
        logger.info(f"Checking if the dataset is locally available at {dataset_path}")
        if os.path.isfile(dataset_path):
            logger.info(f"Data file is locally available at {dataset_path}. Loading the dataset...")
            return self.load_docs_from_json(dataset_path)
        else:
            logger.info(f"Mojo Docs not available locally at {dataset_path}")
            if dataset_variant == 'short':
                return self.create_mojo_docs_short_dataset(
                    [self.config.url.mojo_docs_why_mojo, self.config.url.mojo_docs_faq,
                     self.config.url.mojo_docs_getting_started, self.config.url.mojo_docs_roadmap])
            else:
                return self.create_mojo_docs_dataset(self.config.url.mojo_documentation_home_url,
                                                     self.config.url.mojo_documentation_base_url)
