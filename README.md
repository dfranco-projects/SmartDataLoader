# SmartDataLoader (WIP)

🚀 __SmartDataLoader__ is your intelligent, cutting-edge assistant for effortlessly loading datasets and solving import issues! Built for data practitioners, it goes beyond simple automation by __integrating a powerful LLM-based API RAG (Retriever-Augmented Generation) to help you troubleshoot and resolve data import errors in real time__. Whether you're dealing with formatting challenges or missing metadata, SmartDataLoader will guide you through the process and offer practical solutions, reducing manual effort and speeding up imports.

__Quick imports, intelligent fixes, and interactive support—SmartDataLoader makes dataset loading faster and smarter than ever.__

__Currently supports the file formats: `.csv`, `.xlsx`, `.parquet`, `.json`, and `.txt`.__

---

## Features

__Fast Imports__: SmartDataLoader optimizes your data loading process, cutting down on wait times and enabling you to work with your data faster.
__LLM-Powered Assistant__: Leverage an advanced LLM API to diagnose import issues and provide step-by-step solutions, answering your questions and suggesting fixes in real time.
__Manual Metadata Updates__: While SmartDataLoader automates much of the metadata management, it also allows you to manually update metadata, ensuring accuracy when automated fixes aren't sufficient.
- __Dynamic Metadata Management__:Automatically generate metadata for your files, streamlining imports.
- __Pandas Integration__: Fully compatible with pandas functions, supporting all major pandas file readers (`read_csv`, `read_excel`, etc.).
- __Documentation on Demand__: nstantly retrieve detailed documentation on pandas function arguments based on your file types.

---

## Getting Started

### Repository Structure

```bash
SmartDataLoader/
├── README.md                              # Project overview and usage instructions
├── utils/
│   ├── data_ingestor.py                   # Handles metadata creation and ingestion
│   ├── data_loader.py                     # Loads data using the metadata
│   ├── metadata_handler.py                # Metadata manipulation and updates
│   ├── path_manager.py                    # Centralized path manager
├── assistant/
│   ├── __init__.py                        # Makes the assistant package
│   ├── pandas_doc_helper.py               # Pandas documentation helper
│   ├── import_assistant.py                # Diagnoses and suggests solutions for import issues
├── example_data/
│   ├── clean_data/                        # Clean example data
│       ├── one_file/                      # One example file
│       ├── multiple_files/                # Multiple example files
│   ├── raw_data/                          # Unprocessed example data
├── examples/
│   ├── import_multiple_extensions.ipynb   # Example of loading multiple file types (CSV, XLSX, etc.)
│   ├── metadata_handling.ipynb            # Example of metadata handling using pandas_doc_helper and the assistant
├── requirements.txt                       # Required dependencies
└── .gitignore                             # Files and directories to ignore
```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartDataLoader.git
   cd SmartDataLoader
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ````

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## License

MIT License. See LICENSE file for details.