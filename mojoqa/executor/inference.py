"""
This class is responsible for performing inference and generates the answer for the query.
"""
from langchain.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import DeepLake
from langchain.llms.llamacpp import LlamaCpp
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from mojoqa.utils.config import Config


class Inference:
    """
    Inference class for performing inference and retrieving top-k similar research papers.
    """

    def __init__(self, cfg):
        """
        Constructor method to initialize the Inference class with a given configuration.
        Instantiates necessary objects for Llama embeddings, DeepLake, and data loading.
        Args:
            cfg: Configuration object for the project.
        """
        self.config = Config.from_json(cfg)
        self.embedding_function = LlamaCppEmbeddings(
            model_path=self.config.llama_embedding_model.model_path,
            n_gpu_layers=self.config.llama_embedding_model.n_gpu_layers,
            n_ctx=self.config.llama_embedding_model.n_ctx)
        self.vector_database_obj = DeepLake(dataset_path=self.config.path.vector_store_path,
                                            read_only=True,
                                            embedding=self.embedding_function)
        self.llama_model = LlamaCpp(model_path=self.config.llama_model.model_path,
                                    n_gpu_layers=self.config.llama_model.n_gpu_layers,
                                    n_ctx=self.config.llama_model.n_ctx,
                                    temperature=self.config.llama_model.temperature)
        self.template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        
        Helpful answer: 
        """

    def get_answer(self, input_query: str):
        """
        This function takes as input the query and uses the RAG chain to generate the answer.
        Generated answer is returned.
        Args:
            input_query (str): the input query from the user
        Returns:
            Response generated from the LLM
        """

        prompt = ChatPromptTemplate.from_template(self.template)

        retriever = self.vector_database_obj.as_retriever()
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llama_model
            | StrOutputParser()
        )

        return chain.invoke(input_query)
