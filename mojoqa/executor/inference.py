"""
This class is responsible for performing inference and retrieving top-k similar research papers.
"""
import pandas as pd
from langchain.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import DeepLake
from langchain.llms.llamacpp import LlamaCpp
import numpy as np
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


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
        self.config = cfg
        self.embedding_function = LlamaCppEmbeddings(
            model_path=self.config.model_params.llama_embedding_model.model_path,
            n_gpu_layers=self.config.model_params.llama_embedding_model.n_gpu_layers,
            n_ctx=self.config.model_params.llama_embedding_model.n_ctx)
        self.vector_database_obj = DeepLake(dataset_path=self.config.path.vector_store_path,
                                            read_only=True,
                                            embedding=self.embedding_function)
        self.llama_model = LlamaCpp(model_path=self.config.model_params.llama_model.model_path,
                                    n_gpu_layers=self.config.model_params.llama_model.n_gpu_layers,
                                    n_ctx=self.config.model_params.llama_model.n_ctx,
                                    temperature=self.config.model_params.llama_model.temperature)
        self.template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        
        Helpful answer: 
        """

    def get_context_from_vector_store(self, k: int, input_query: str):
        # result = self.vector_database_obj.similarity_search_with_score(
        #     input_query,
        #     distance_metric="cos",
        #     k=k)

        prompt = ChatPromptTemplate.from_template(self.template)

        # qa = RetrievalQA.from_chain_type(
        #     llm=self.llama_model,
        #     chain_type="stuff",
        #     retriever=self.vector_database_obj.as_retriever(),
        # )

        retriever = self.vector_database_obj.as_retriever()
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llama_model
            | StrOutputParser()
        )

        print(chain.invoke(input_query))
        #
        #
        # answer = qa.run(input_query)
        # print(answer)

        return ""
