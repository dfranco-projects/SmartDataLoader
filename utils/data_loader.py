import os
import sys
import json
import pandas as pd
from IPython import get_ipython
from IPython.display import display
from path_manager import PathManager

class DataLoader:
    def __init__(self, metadata_path: str = None) -> None:
        '''
        Initializes the DataLoader with the path to the metadata file.

        Args:
            metadata_path (str, optional): Path to the folder containing the metadata JSON file.
                                        If not provided, the default path from PathManager will be used.
        '''
        # Instantiate PathManager in case no folder paths are provided
        path_manager = PathManager()

        self.metadata_file_path = os.path.join(metadata_path, 'metadata.json') or os.path.join(path_manager.get_metadata_path(), 'metadata.json')
        self.metadata = self.load_metadata()

    def load_metadata(self) -> dict:
        '''
        Load metadata from the given JSON file.

        Returns:
            dict: Loaded metadata.

        Raises:
            Exception: If there is an error loading the metadata.
        '''
        try:
            with open(self.metadata_file_path, 'r') as metadata_file:
                metadata = json.load(metadata_file)
            
            # Count the number of files
            print('There is 1 file in the input data folder.\n' if len(metadata) == 1 else f'There are {len(metadata)} files input data folder.\n')
            return metadata
        except Exception as e:
            raise Exception(f'Error loading metadata: {e}')

    def load_data(self) -> dict | pd.DataFrame:
        '''
        Load data based on the metadata instructions.

        Returns:
            dict: Dictionary of loaded DataFrames if multiple files are provided, file names are the key to access.
            pd.DataFrame: A single DataFrame if only one file is provided.

        Raises:
            Exception: If any error occurs while loading the data.
        '''
        def in_notebook() -> bool:
            '''Check if running in a Jupyter environment.'''
            try:
                from IPython import get_ipython
                if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
                    return False
            except ImportError:
                return False
            except AttributeError:
                return False
            return True
        
        def display_or_print(message: str, df: pd.DataFrame) -> None:
            '''
            Display or print a message and the first few rows of a DataFrame.

            If the code is running in a Jupyter environment, the message is printed
            and the DataFrame is displayed as an HTML table using the `display` function.
            Otherwise, the message is printed, and the DataFrame's head is printed as plain text.

            Args:
                message (str): A message to accompany the displayed or printed DataFrame.
                df (pd.DataFrame): The DataFrame to display or print.
            '''
            if in_notebook():
                print(message)
                display(df.head().style)
            else:
                print(message)
                print(df.head())

        # Determine if we're dealing with a single or multiple files
        singular_file = len(self.metadata) == 1

        # List to store multiple dataframes if necessary
        dfs = {}
        # Iterate over metadata and load the data
        for entry in self.metadata:
            try:
                # Extract file name, and import instructions (function and arguments)
                file_name = entry.get('file_name')
                import_function = entry['import_instructions']['function']
                import_args = entry['import_instructions']['arguments']

                # Dynamically call the pandas function
                df = eval(import_function)(**import_args)

                # Display or print based on the environment
                if singular_file:
                    message = f'\nLoaded \033[1m{file_name}\033[0m with {len(df)} rows and {len(df.columns)} features.'
                    display_or_print(message, df)
                else:
                    message = f'\nLoaded \033[1m{file_name}\033[0m with {len(df)} rows and {len(df.columns)} features.'
                    display_or_print(message, df)
                    dfs[file_name] = df

            except Exception as e:
                raise Exception(f'Failed to load data from {file_name}: {e}')

        return df if singular_file else dfs


if __name__ == '__main__': 
    from path_manager import PathManager
    from data_ingestor import DataFactory
    from data_loader import DataLoader

    # Set the project root path by going one level up from the 'utils' folder
    root_path = os.path.abspath(os.path.join(os.getcwd(), '..'))

    # Set up the data path, in this example the data in the example_data folder within the clean_data
    data_folder_name = os.path.join('example_data', 'clean_data', 'one_file')

    # Set up the path manager instance
    path_manager_instance = PathManager(root_path=root_path, data_folder=data_folder_name)

    print(
        f'Root path: {path_manager_instance.get_project_root()}\n'
        f'Data path: {path_manager_instance.get_data_path()}\n'
        f'Metadata path: {path_manager_instance.get_metadata_path()}\n'
        f'Extracted Data path: {path_manager_instance.get_extracted_data_path()}'
    )

    # Set up the data factory ingestor instance
    ingestor = DataFactory(
        data_path = path_manager_instance.get_data_path(),
        metadata_path = path_manager_instance.get_metadata_path(),
        extracted_data_path = path_manager_instance.get_extracted_data_path()
    )

    ingestor.run_ingestion()

    # Set up the data loader instance
    data_loader_instance = DataLoader(path_manager_instance.get_metadata_path())
    df = data_loader_instance.load_data()