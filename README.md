# **DataRanger (WIP)**  
🚀 **AI-Powered Data Loading and Preprocessing Assistant**  

**DataRanger** is your smart AI assistant for loading and preprocessing datasets, solving import issues, and handling data transformations with ease! Designed for data practitioners, it goes far beyond simple automation by **integrating a powerful LLM-based RAG (Retriever-Augmented Generation)** built from scratch. This cutting-edge system helps you troubleshoot, resolve data import errors in real time, and apply advanced preprocessing solutions to your data.  

Whether you're dealing with formatting challenges, missing metadata, or complex transformations, **DataRanger** guides you through the process with practical solutions, reducing manual effort and speeding up your workflows.  

**Quick imports, intelligent fixes, and interactive support**—DataRanger makes dataset preparation smarter, faster, and more efficient.  

---

## **Features**  

- **Fast Imports**: Optimizes your data loading process, cutting down on wait times and enabling you to work with your data faster.  
- **LLM-Powered Assistant**: Leverage an advanced LLM API to diagnose import issues and provide step-by-step solutions, answering your questions and suggesting fixes in real time.  
- **Manual Metadata Updates**: Automates much of the metadata management while allowing manual updates for precision when needed.  
- **Dynamic Metadata Management**: Automatically generates metadata for your files, streamlining imports.  
- **Pandas Integration**: Fully compatible with pandas functions, supporting all major pandas file readers (`read_csv`, `read_excel`, etc.).  
- **Documentation on Demand**: Instantly retrieve detailed documentation on pandas function arguments based on your file types.  
- **Advanced Preprocessing**: Handles preprocessing tasks, such as data type corrections, feature engineering, and cleaning, all guided by the LLM.  

---

## **Why a RAG?**  

DataRanger is powered by a **Retriever-Augmented Generation (RAG)** system built from scratch that combines the power of LLMs with a custom-built retrieval module. This architecture ensures that:  
- The assistant can fetch relevant solutions from trusted sources (e.g., documentation, user-provided metadata, or even external resources).  
- It adapts dynamically to handle unseen errors or preprocessing challenges.  
- It enables intelligent interactions with your scripts and datasets for personalized, actionable insights.  

---

## **Supported File Formats**  

- `.csv`  
- `.xlsx`  
- `.parquet`  
- `.json`  
- `.txt`  

---

## **Get Inspired**  

SmartDataPrep is more than just a tool—it's a learning resource. Explore the codebase to understand how to build a RAG system from scratch for your own projects!  

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