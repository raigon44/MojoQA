"""
VectorStore Class

This class is responsible for creating a vector store of document chunks using the LangChain library.
"""

from langchain.embeddings import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.deeplake import DeepLake
from mojoqa.utils.logger import logger
from mojoqa.dataloader.dataloader import DataLoader


class VectorStore:
    """
    VectorStore class for creating a vector store of document chunks.
    """

    def __init__(self, cfg):
        """
        Constructor to initialize the VectorStore with a given configuration.
        Instantiates necessary objects for data loading, embedding, and text splitting.
        Args:
            cfg: Configuration object for the project.
        """
        self.config = cfg
        self.data_loader = DataLoader(self.config)
        self.embedding_function = LlamaCppEmbeddings(model_path=self.config.model_params.llama_embedding_model.model_path,
                                                     n_gpu_layers=self.config.model_params.llama_embedding_model.n_gpu_layers,
                                                     n_ctx=self.config.model_params.llama_embedding_model.n_ctx)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.config.document_splitter.chunk_size,
                                                            chunk_overlap=self.config.document_splitter.chunk_overlap)

    def create_documents(self) -> list:
        """
        Creates a list of document objects from preprocessed text documents.
        Retrieves paper titles, preprocesses documents, and splits them into chunks.
        Returns:
            list: List of document objects.
        """
        document_obj_list = []
        logger.info("Loading the Mojo Documentation frame")
        array_of_documents = self.data_loader.load_mojo_docs_dataset()
        array_of_documents = [[doc] for doc in array_of_documents]
        doc_count = 0
        for doc in array_of_documents:
            document_chunks = self.text_splitter.split_documents(doc)

            for doc_chunk in document_chunks:
                doc_chunk.metadata['id'] = doc_count

            document_obj_list.extend(document_chunks)
            doc_count += 1

        return document_obj_list

    def create_vector_store(self):
        """
        Creates a vector store from the generated document chunks.
        Uses DeepLake to generate a vector store with Llama embeddings.
        Returns:
            Object to access the created vector store.
        """
        documents = self.create_documents()
        db = DeepLake.from_documents(documents, self.embedding_function,
                                     dataset_path=self.config.path.vector_store_path, overwrite=True)
        return db


