import pandas as pd
import requests
from mojoqa.config.config import CFGLog
from mojoqa.utils.config import Config
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader


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
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return -1

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

    def create_mojo_docs_dataset(self, home_page_url: str, base_url: str):
        relevant_links_dict = self.get_sub_page_links(home_page_url, base_url)

        url_loader = UnstructuredURLLoader(urls=list(relevant_links_dict.keys()))
        html_doc = url_loader.load()

        html_page_data = [doc.page_content for doc in html_doc]
        src = [doc.metadata['source'] for doc in html_doc]

        mojo_docs_data = {
            'id': list(range(len(html_page_data))),
            'page_content': html_page_data,
            'src': src
        }

        mojo_docs_data_frame = pd.DataFrame(mojo_docs_data)

        return mojo_docs_data_frame


if __name__ == "__main__":
    config = Config.from_json(CFGLog)
    data_obj = DataLoader(config.data)
    data_frame = data_obj.create_mojo_docs_dataset(
        'https://docs.modular.com/mojo/', 'https://docs.modular.com/')
    print(len(data_frame))
    data_frame.to_csv('data.csv')
