'''
Data Ingestor
=============

This script provides functionalities to streamline data ingestion processes, including:

1. Generating and saving metadata for each file to enable faster subsequent imports.
2. Extracting files from zip archives and organizing them for easier access.

The metadata saved by this script typically includes file-specific details such as:
- File path
- File type
- Columns name
- Number of rows
- Loading instructions

**Key Features:**
- Centralized path management for project directories.
- Support for multiple file formats (`.csv`, `.xlsx`, `.parquet`, `.json`, `.txt`).
- Modular design with classes for handling specific file types.

**Setup Instructions:**
1. Edit the `PathManager` class paths to match your folder structure.

**ATTENTION:**  
Ensure the folder structure is correct to avoid errors.
'''
import os
import json
import zipfile
import warnings
import pandas as pd
from abc import ABC, abstractmethod
from path_manager import PathManager

# Define data ingestor interface instance
class DataIngestor(ABC):
    '''
    A class to handle data ingestion tasks, including file extraction and metadata management.
    '''
    @abstractmethod
    def ingest(self, file_path: str) -> dict:
        '''
        Reads and generates loading instructions for different file types.

        Args:
            file_path (str): Path of the original data file.
            file_extension (str): File type.
        
        Returns: 
            dict: A dictionary containing metadata from the file.
        '''
        pass

    @staticmethod
    def read_file(file_path: str, file_extension: str) -> tuple[pd.DataFrame, dict]:
        '''
        Reads and generates loading instructions for different file types.

        Args:
            file_path (str): Path of the original data file.
            file_extension (str): File type.

        Returns:
            tuple: A tuple containing a pandas dataframe and a dictionary with metadata for each file extracted.

        '''
        
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
            import_instructions = {
                'function': 'pd.read_csv',
                'arguments': {'filepath_or_buffer': file_path}
            }

        elif file_extension == '.xlsx':
            df = pd.read_excel(file_path)
            import_instructions = {
                'function': 'pd.read_excel',
                'arguments': {'io': file_path}
            }

        elif file_extension == '.parquet':
            df = pd.read_parquet(file_path)
            import_instructions = {
                'function': 'pd.read_parquet',
                'arguments': {'path': file_path}
            }

        elif file_extension == '.json':
            df = pd.read_json(file_path)
            import_instructions = {
                'function': 'pd.read_json',
                'arguments': {'path_or_buf': file_path}
            }

        elif file_extension == '.txt':
            df = pd.read_csv(file_path, delimiter='\t')
            import_instructions = {
                'function': 'pd.read_csv',
                'arguments': {'filepath_or_buffer': file_path, 'delimiter': '\t'}
            }
        else:
            raise ValueError(f'Unsupported file type: {file_extension}')

        return df, import_instructions

# Define a specific data ingestor for zip ingestion
class ZipDataIngestor(DataIngestor):
    def __init__(self, extracted_data_path: str) -> None:
        self.extracted_data_path = extracted_data_path

    def ingest(self, file_path: str) -> dict:
        '''
        Handles ingestion and extraction of ZIP archives.

        Args:
            file_path (str): Path to the .zip file to be extracted and ingested.

        Returns:
            dict: A dictionary containing metadata of each file extracted from the .zip.
        '''
        if not file_path.endswith('.zip'):
            raise ValueError('Provided file is not a .zip archive.')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File {file_path} does not exist.')
        
        # Specify extracted data directory (updated to use PathManager)
        extracted_data_folder = self.extracted_data_path

        # Ensure a folder for the extracted exists otherwise it creates one
        os.makedirs(extracted_data_folder, exist_ok=True)

        # Extract .zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_data_folder)

        # List extracted files
        extracted_files = os.listdir(extracted_data_folder)
        filtered_extracted_files = [i for i in extracted_files if not i.startswith('.') and not i.startswith('_')]
        if not filtered_extracted_files:
            raise FileNotFoundError('No files found within the .zip file.')

        # Supported formats
        supported_formats = {'.csv', '.xlsx', '.parquet', '.json', '.txt'}
        metadata = []

        for file_name in filtered_extracted_files:
            extracted_file_path = os.path.join(extracted_data_folder, file_name)
            file_extension = os.path.splitext(file_name)[1]

            if file_extension not in supported_formats:
                warnings.warn(f'Unsupported file type: {file_name}. Skipping.')
                continue
                
            try:
                df, import_instructions = DataIngestor.read_file(extracted_file_path, file_extension)

                # Add metadata for the file
                metadata.append({
                    'file_name': file_name,
                    'file_type': file_extension,
                    'columns': df.columns.tolist(),
                    'row_count': len(df),
                    'import_instructions': import_instructions
                })
            except Exception as e:
                warnings.warn(f'Failed to process {file_name}: {e}')

        return metadata

# Define a specific data ingestor for csv ingestion
class CsvDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> dict:
        '''
        Reads a CSV file and generates metadata.

        Args:
            file_path (str): Path to the CSV file to be ingested.

        Returns:
            dict: Metadata from the CSV file.
        '''

        # Ensure the file is a CSV
        if not file_path.endswith('.csv'):
            raise ValueError('The provided file is not a CSV file.')

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'The file {file_path} does not exist.')

        try:
            df, import_instructions = DataIngestor.read_file(file_path, '.csv')

            # Generate metadata
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_type': '.csv',
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'import_instructions': import_instructions
            }
            return metadata

        except Exception as e:
            raise ValueError(f'Failed to ingest CSV file: {e}')

# Define a specific data ingestor for excel ingestion
class ExcelDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> dict:
        '''
        Reads an Excel file and generates metadata.

        Args:
            file_path (str): Path to the Excel file.

        Returns:
            dict: Metadata from the Excel file.
        '''
        if not file_path.endswith(('.xlsx', '.xls')):
            raise ValueError('The provided file is not an Excel file.')

        try:
            df, import_instructions = DataIngestor.read_file(file_path, '.xlsx')

            # Generate metadata
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_type': '.xlsx',
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'import_instructions': import_instructions
            }
            return metadata

        except Exception as e:
            raise ValueError(f'Failed to ingest Excel file: {e}')

# Define a specific data ingestor for parquet ingestion
class ParquetDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> dict:
        '''
        Reads a Parquet file and generates metadata.

        Args:
            file_path (str): Path to the Parquet file.

        Returns:
            dict: Metadata from the Parquet file.
        '''
        if not file_path.endswith('.parquet'):
            raise ValueError('The provided file is not a Parquet file.')

        try:
            df, import_instructions = DataIngestor.read_file(file_path, '.parquet')

            # Generate metadata
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_type': '.parquet',
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'import_instructions': import_instructions
            }
            return metadata

        except Exception as e:
            raise ValueError(f'Failed to ingest Parquet file: {e}')

# Define a specific data ingestor for JSON ingestion
class JsonDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        '''
        Reads a JSON file and generates metadata.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            pd.DataFrame: Metadata from the JSON file.
        '''
        if not file_path.endswith('.json'):
            raise ValueError('The provided file is not a JSON file.')

        try:
            df, import_instructions = DataIngestor.read_file(file_path, '.json')

            # Generate metadata
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_type': '.parquet',
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'import_instructions': import_instructions
            }
            return metadata

        except Exception as e:
            raise ValueError(f'Failed to ingest Parquet file: {e}')

# Define a specific data ingestor for txt ingestion
class TxtDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        '''
        Reads a tab-delimited TXT file and generates metadata.

        Args:
            file_path (str): Path to the TXT file.

        Returns:
            dict: Metadata from the TXT file.
        '''
        if not file_path.endswith('.txt'):
            raise ValueError('The provided file is not a TXT file.')
        
        try:
            df, import_instructions = DataIngestor.read_file(file_path, '.json')

            # Generate metadata
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_type': '.json',
                'columns': df.columns.tolist(),
                'row_count': len(df),
                'import_instructions': import_instructions
            }
            return metadata

        except Exception as e:
            raise ValueError(f'Failed to ingest TXT file: {e}')
    
# Define a factory to implement Data Ingestors
class DataFactory:
    def __init__(self, data_path: str = None, metadata_path: str = None, extracted_data_path: str = None) -> None:
        # Instantiate PathManager in case no folder paths are provided
        path_manager = PathManager()

        self.data_path = data_path or path_manager.get_data_path()
        self.metadata_path = metadata_path or path_manager.get_metadata_path()
        self.extracted_data_path = extracted_data_path or path_manager.get_extracted_data_path()

    def save_metadata(self, metadata: dict) -> None:
        '''
        Saves metadata to a JSON file.

        Args:
            metadata (dict): Metadata dictionary.
        '''       
        metadata_dir = self.metadata_path

        # Ensure a folder for metadata exists otherwise it creates one
        os.makedirs(metadata_dir, exist_ok=True)

        # Metadata file path
        metadata_path = os.path.join(metadata_dir, 'metadata.json')

        # Save JSON file
        try:
            with open(metadata_path, 'w') as metadata_file:
                json.dump(metadata, metadata_file, indent=4)
            print(f'Metadata saved at {metadata_path}')
        except Exception as e:
            warnings.warn(f'Failed to save metadata: {e}')

    def get_ingestor(self, file_extension: str) -> DataIngestor:
        '''
        Returns the ingestor for the specified file type.

        Args:
            file_extension (str): The extension of the data file (e.g., '.csv', '.xlsx').

        Returns:
            DataIngestor: An instance of the corresponding data ingestor class for the given file extension.
        
        Raises:
            ValueError: If the provided file extension is currently not supported.
        '''
        ingestors = {
            '.zip': ZipDataIngestor(extracted_data_path=self.extracted_data_path),
            '.csv': CsvDataIngestor(),
            '.xlsx': ExcelDataIngestor(),
            '.parquet': ParquetDataIngestor(),
            '.json': JsonDataIngestor(),
            '.txt': TxtDataIngestor()
        }
        
        if file_extension not in ingestors:
            raise ValueError(f'Unsupported file type: {file_extension}')
        
        return ingestors[file_extension]

    def run_ingestion(self) -> None:
        '''
        High-level function to handle the ingestion process. It selects the files from
        the provided directory, identifies the file extensions, and runs the ingestion
        process to extract metadata for each file.

        Returns:
            None: Saves the metadata JSON file in the metadata folder.
        '''
        data_folder = self.data_path

        # Filter files (ignore hidden & cache files)
        filtered_files = [
            os.path.join(data_folder, f) 
            for f in os.listdir(data_folder) 
            if not f.startswith('.') and not f.startswith('_')
        ]

        # Get the file extensions
        file_extensions = [os.path.splitext(f)[1] for f in filtered_files]

        # Initialize data ingestors based on file extensions
        ingestors = [self.get_ingestor(ext) for ext in file_extensions]

        # Ingest data and collect metadata
        metadata_list = []
        for ingestor, file_path, file_extension in zip(ingestors, filtered_files, file_extensions):
            metadata = ingestor.ingest(file_path)

            if file_extension != '.zip': 
                metadata_list.append(metadata)
            else:
                metadata_list.extend(metadata)

        # Save metadata
        self.save_metadata(metadata_list)
        
        print('Data was successfully ingested.')

if __name__ == '__main__':

    # ingestor = DataFactory()
    # ingestor.run_ingestion()

    pass