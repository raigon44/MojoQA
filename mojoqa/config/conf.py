"""Model configurations in json format.
Paths are always relative to the location of the command line,
paths are not relative to any objects in the source codes.
If you are not running scripts from the root folder (e.g., using cd instead),
then the paths here need to be checked and modified accordingly"""

CFGLog = {
    "path": {
        "vector_store_path": "./data/db",
        "log": "./log"
    },
    "llama_embedding_model": {
            "model_path": "./models/llama-2-7b.Q4_K_S.gguf",
            "n_gpu_layers": 32,
            "n_ctx": 1024,
    },
    "llama_model": {
            "model_path": "./models/llama-2-7b-chat.Q4_K_S.gguf",
            "n_gpu_layers": 32,
            "n_ctx": 4096,
            "temperature": 0,
            "top_k": 40,
            "top_p": 0.1,
    },
    "document_splitter": {
        "chunk_size": 1000,
        "chunk_overlap": 15,
    }
}