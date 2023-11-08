"""Model configurations in json format.
Paths are always relative to the location of the command line,
paths are not relative to any objects in the source codes.
If you are not running scripts from the root folder (e.g., using cd instead),
then the paths here need to be checked and modified accordingly"""

CFGLog = {
    "data": {
        "extracted_html_files_path": "./data/extractedData/",
        "raw_html_files_path": "./data/raw_data/",
        "preprocessed_data_path": "./data/preprocessed_data/",
        "vector_store_dataset_path": "./data/db",
        "title_summary_csv_file": "./data/summaries/title_frame.csv",
        "mojo_documentation_base_url": "https://docs.modular.com/mojo/"
    },
    "llama_embedding_model": {
            "model_path": "./models/llama-2-7b.Q4_K_S.gguf",
            "n_gpu_layers": 32,
            "n_ctx": 1024,
    },
    "document_splitter": {
        "chunk_size": 1000,
        "chunk_overlap": 15,
    }
}
