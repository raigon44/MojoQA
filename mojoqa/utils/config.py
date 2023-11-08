"""Config class"""
import json


class Config:
    """Config class which contains all configurable parameter for this project"""

    def __init__(self, data, llama_embedding_model, document_splitter):
        """
        Constructor method to initialize the Config class with specified parameters.
        """
        self.data = data
        self.llama_embedding_model = llama_embedding_model
        self.document_splitter = document_splitter

    @classmethod # using config to define constructor of the class
    def from_json(cls, cfg):
        """Class method to create a Config instance from a JSON object.
           Uses a HelperDict class to convert JSON into a Python object"""
        params = json.loads(json.dumps(cfg), object_hook=HelperDict)
        # init all class instance with all configuration parameters
        return cls(params.data, params.llama_embedding_model, params.document_splitter)


class HelperDict(object):
    """Helper class to convert a dictionary into a Python object"""
    def __init__(self, dict_):
        self.__dict__.update(dict_)