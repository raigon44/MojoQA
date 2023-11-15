from mojoqa.executor.vectorstore import VectorStore
import hydra
from hydra.core.config_store import ConfigStore
from mojoqa.config.config import MojoQAConfig


def create_vector_store(cfg):
    """
       Initializes a VectorStore object and creates a vector store containing document chunks embeddings.
    """
    vector_db_obj = VectorStore(cfg)
    db = vector_db_obj.create_vector_store()
    return


config_store = ConfigStore.instance()
config_store.store(name="mojoqa_config", node=MojoQAConfig)


@hydra.main(config_path='../config', config_name="config")
def main(cfg: MojoQAConfig):
    """
        Executes the process of creating a vector store.
    """
    create_vector_store(cfg)
    return


if __name__ == '__main__':
    main()

