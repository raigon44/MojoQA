from dataclasses import dataclass


@dataclass
class Path:
    mojo_docs_dataset_path: str
    mojo_docs_short_dataset_path: str
    vector_store_path: str
    log: str


@dataclass
class Url:
    mojo_documentation_home_url: str
    mojo_documentation_base_url: str
    mojo_docs_why_mojo: str
    mojo_docs_faq: str
    mojo_docs_getting_started: str
    mojo_docs_roadmap: str


@dataclass
class LlamaEmbeddingModel:
    model_path: str
    n_gpu_layers: int
    n_ctx: int


@dataclass
class LlamaModel:
    model_path: str
    n_gpu_layers: int
    n_ctx: int
    # max_token: int
    temperature: float
    top_k: int
    top_p: float


@dataclass
class ModelParams:
    llama_embedding_model: LlamaEmbeddingModel
    llama_model: LlamaModel


@dataclass
class DocumentSplitter:
    chunk_size: int
    chunk_overlap: int


@dataclass
class MojoQAConfig:
    path: Path
    url: Url
    model_params: ModelParams
    document_splitter: DocumentSplitter



